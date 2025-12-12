import chainlit as cl
import sqlite3
import os  # <-- Necessary for accessing environment variables
from pydantic_ai import Agent, RunContext
from langfuse import get_client
import numpy as np
import pickle
from dotenv import load_dotenv
from typing import List, Tuple
from voyageai.client import Client
from sklearn.metrics.pairwise import cosine_similarity
from google import genai
from google.genai import types
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from tavily import TavilyClient
import torch
import warnings

# =========================================================
# 1. GLOBAL SETUP AND CONFIGURATION (RUNS ONCE)
# =========================================================

# Load environment variables FIRST
load_dotenv()

# RAG Configuration Constants (Defined once)
VECTOR_STORE_FILENAME = "pokemon_vector_store_paragraph.pkl"
TOP_K_RETRIEVAL = 20 # Number of chunks to retrieve initially before reranking
TOP_N_RERANK = 5     # Number of chunks to keep after reranking (the final context size)
RERANKER_MODEL_NAME = 'cross-encoder/ms-marco-MiniLM-L-6-v2'

# Initialize API Clients
google_api_key = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=google_api_key)

voyage_api_key = os.getenv("VOYAGE_API_KEY")
VOYAGE_CLIENT = Client(api_key="Your API Key Here")

tavily_api_key = os.getenv("TAVILY_API_KEY")
TAVILY_CLIENT = TavilyClient(api_key=tavily_api_key)

# Reranker Model Loading (MUST be before GLOBAL_CHUNKS)
warnings.filterwarnings("ignore")
RERANKER_TOKENIZER = None
RERANKER_MODEL = None

try:
    print(f"RAG: Loading Reranker Model: {RERANKER_MODEL_NAME}...")
    RERANKER_TOKENIZER = AutoTokenizer.from_pretrained(RERANKER_MODEL_NAME)
    RERANKER_MODEL = AutoModelForSequenceClassification.from_pretrained(RERANKER_MODEL_NAME)
    print("RAG: Reranker Model loaded successfully.")
except Exception as e:
    print(f"RAG WARNING: Reranker Model skipped. Error: {e}")

# =========================================================
# 2. TOOL AND HELPER FUNCTION DEFINITIONS
# =========================================================

def get_pokedex_schema() -> str:
    """
    Returns the schema of the Pokemon database.
    Call this first to understand the table structure before writing queries.
    """
    return """
    The database 'pokedex.db' has 3 tables:

    1. pokemon
       - Columns: 
           pokedex_id (INTEGER PK), 
           name (TEXT), 
           type_1 (TEXT, NOTE: MUST USE 'type_1' WITH AN UNDERSCORE), 
           type_2 (TEXT, NOTE: MUST USE 'type_2' WITH AN UNDERSCORE), 
           base_hp (INTEGER), 
           is_legendary (BOOLEAN)

    2. moves
       - Columns: move_id (INTEGER PK), move_name (TEXT), move_type (TEXT), power (INTEGER), accuracy (INTEGER)

    3. pokemon_moveset (Linking Table)
       - Columns: pokemon_id (FK to pokemon.pokedex_id), move_id (FK to moves.move_id)
       - NOTE: THE TABLE NAME FOR MOVES IS 'pokemon_moveset', NOT 'pokemon_moves'.
       - Use this to join Pokemon with their Moves.
    """

def query_pokedex(sql_query: str) -> str:
    """
        Executes a SQL query against the Pokedex database.
        Input must be a valid SQL string starting with SELECT.
        """
    # 1. Safety: Enforce Read-Only at the String Level
    forbidden = ["INSERT", "UPDATE", "DELETE", "DROP", "ALTER"]
    if any(word in sql_query.upper() for word in forbidden):
        return "Error: This tool is for READ access only."

    # 2. Connection: Enforce Read-Only at the Driver Level
    try:
        # uri=True enables the query parameters like mode=ro
        uri = 'file:pokedex.db?mode=ro'
        conn = sqlite3.connect(uri, uri=True)
        cursor = conn.cursor()

        # Execute
        cursor.execute(sql_query)
        rows = cursor.fetchall()

        # Get column names for better readability
        column_names = [description[0] for description in cursor.description]

        conn.close()

        if not rows:
            return "Query executed successfully but returned 0 results."

        # Format as a list of dictionaries so the LLM understands the data mapping
        results = [dict(zip(column_names, row)) for row in rows]
        return str(results)

    except sqlite3.Error as e:
        return f"Database Error: {e}"


def load_vector_store() -> Tuple[List[str], np.ndarray]:
    """Loads the pre-embedded chunks and embeddings."""
    try:
        with open(VECTOR_STORE_FILENAME, 'rb') as f:
            vector_store = pickle.load(f)

        chunks = [item[0] for item in vector_store]
        embeddings = np.array([item[1] for item in vector_store])
        print(f"RAG: Loaded {len(chunks)} chunks from {VECTOR_STORE_FILENAME}.")
        return chunks, embeddings
    except FileNotFoundError:
        print(f"RAG ERROR: Vector store file '{VECTOR_STORE_FILENAME}' not found.")
        return [], np.array([])
    except Exception as e:
        print(f"RAG ERROR during load: {e}")
        return [], np.array([])


def embed_query(query: str) -> np.ndarray:
    """Embeds the user's query using Voyage AI."""
    # VOYAGE_CLIENT is global
    response = VOYAGE_CLIENT.embed(
        [query],  # Input must be a list
        model="voyage-3.5",
        input_type="query"
    )

    # Return the single embedding vector as a NumPy array
    return np.array(response.embeddings[0])


def search_chunks(query_embedding: np.ndarray, k: int = TOP_K_RETRIEVAL) -> List[Tuple[str, float]]:
    """
    Finds the k closest chunks to the query using cosine similarity.
    Returns a list of (chunk_text, similarity_score).
    """
    # GLOBAL_EMBEDDINGS is global
    if GLOBAL_EMBEDDINGS.size == 0:
        return []

    # Calculate cosine similarity between the query and all chunk embeddings
    similarities = cosine_similarity(query_embedding.reshape(1, -1), GLOBAL_EMBEDDINGS)[0]

    # Get the indices of the top k most similar chunks (descending order)
    top_k_indices = np.argsort(similarities)[::-1][:k]

    # Compile the results: list of (chunk_text, score)
    results = [
        (GLOBAL_CHUNKS[i], similarities[i]) # GLOBAL_CHUNKS is global
        for i in top_k_indices
    ]
    return results


def rerank_chunks(query: str, retrieved_chunks: List[Tuple[str, float]], n: int = TOP_N_RERANK) -> List[str]:
    """
    Uses a cross-encoder model to re-score and select the top N most relevant chunks.
    Returns a list of the top N chunk texts.
    """
    # RERANKER_MODEL, RERANKER_TOKENIZER are global
    if RERANKER_MODEL is None:
        print("RAG RERANKER SKIPPED: Returning top retrieved chunks.")
        return [chunk for chunk, score in retrieved_chunks[:n]]

    print(f"RAG RERANKER: Scoring {len(retrieved_chunks)} chunks for final selection.")

    # 1. Prepare pairs for the cross-encoder: (query, chunk_text)
    pairs = [(query, chunk) for chunk, score in retrieved_chunks]

    # 2. Tokenize the pairs
    features = RERANKER_TOKENIZER(pairs, padding=True, truncation=True, return_tensors='pt')

    # 3. Get scores from the model
    RERANKER_MODEL.eval()
    with torch.no_grad():
        scores = RERANKER_MODEL(**features).logits.squeeze(dim=-1)

    # 4. Combine chunks and their new scores, then sort
    reranked_results = sorted(
        zip(retrieved_chunks, scores.tolist()),
        key=lambda x: x[1],
        reverse=True
    )

    # 5. Extract the top N chunk texts
    top_n_chunks = [item[0][0] for item in reranked_results[:n]]

    print(f"RAG RERANKER: Final Context Chunks selected: {len(top_n_chunks)}")
    return top_n_chunks


def generate_answer(query: str, context_chunks: List[str], gemini_client: genai.Client) -> str:
    """
    Formats the prompt with the retrieved context and sends it to the Gemini LLM
    for final answer synthesis.
    """
    if not context_chunks:
        return "I found no relevant documentation to answer your question."

    context_str = "\n---\n".join(context_chunks)

    SYSTEM_INSTRUCTION = (
        "You are a factual, concise RAG system specializing in documentation. "
        "Your task is to answer the user's question ONLY using the text provided in the <CONTEXT> section below. "
        "If the answer cannot be found in the provided context, you MUST state, 'The answer is not available in the provided documentation.'"
    )

    USER_PROMPT = f"""
    <CONTEXT>
    {context_str}
    </CONTEXT>

    USER QUESTION: {query}
    """

    try:
        # gemini_client is the globally defined 'client' passed in
        response = gemini_client.models.generate_content(
            model='gemini-2.5-flash',
            contents=USER_PROMPT,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION
            )
        )

        return response.text

    except Exception as e:
        return f"LLM Generation Error: Could not reach Gemini API. Details: {e}"


def rag_tool(query: str) -> str:
    """
    Retrieval-Augmented Generation (RAG) tool.
    Performs search, reranking, and LLM synthesis to answer the query based on documentation.
    """
    global client # Access the globally defined Gemini client

    # 1. Query Embedding
    query_emb = embed_query(query)

    # 2. Find top K embeddings (Search)
    retrieved_chunks_with_scores = search_chunks(query_emb, TOP_K_RETRIEVAL)

    if not retrieved_chunks_with_scores:
        return generate_answer(query, [], client)

    # 3. Pass top K embeddings into reranker
    reranked_chunks = rerank_chunks(query, retrieved_chunks_with_scores, TOP_N_RERANK)

    # 4. Pass top N chunks and query to LLM for final answer synthesis
    final_answer = generate_answer(query, reranked_chunks, client)

    return final_answer


def web_search_tavily(query: str) -> str:
    """
    Performs a real-time web search for current events, modern theories,
    or information not found in the agent's internal knowledge bases.
    Returns a summarized text context for the LLM to use.
    """
    global TAVILY_CLIENT

    print(f"TOOL CALL: Performing Tavily Web Search for: {query}")

    try:
        # get_search_context summarizes the top search results into one clean text
        context = TAVILY_CLIENT.get_search_context(
            query=query,
            search_depth="basic", # 'basic' is usually fast and sufficient for LLMs
            max_tokens=4000
        )

        if not context or "not found" in context.lower():
             return f"Tavily search for '{query}' returned no relevant results or data."

        return context

    except Exception as e:
        return f"Tavily Web Search Error: Could not execute search. Details: {e}"


# =========================================================
# 3. GLOBAL DATA INITIALIZATION
# =========================================================

# This must run after the tool functions are defined but before the Agent is created.
GLOBAL_CHUNKS, GLOBAL_EMBEDDINGS = load_vector_store()


# =========================================================
# 4. AGENT SETUP
# =========================================================

langfuse = get_client()
Agent.instrument_all()


# Create basic agent
agent = Agent(
    model='google-gla:gemini-2.5-flash',
    system_prompt=(
    "You are Pokemon GPT, a helpful AI chatbot for gamers learning about the original 151 pokemon. "
    "You have access to a Pokedex Database for structured data (stats, moves, types) and Professor Oak's "
    "Research Documents (RAG tool) for biological, lore, and strategy information. Always use the RAG tool "
    "for questions that cannot be answered with a simple SQL query. Refer to the database schema for exact column names."
),
tools=[get_pokedex_schema, query_pokedex, rag_tool, web_search_tavily],
instrument=True)

# =========================================================
# 5. CHAINLIT HANDLERS
# =========================================================

@cl.on_chat_start
async def start_chat():
    """
    Initializes the chat session, sets history, and provides starter messages.
    """
    # 1. Starters for each tool
    starters = [
        {"label": "Pokedex SQL Starter", "message": "What is the base HP of Bulbasaur?"},
        {"label": "RAG Lore Starter", "message": "Explain the Magikarp Paradox."},
        {"label": "Search the Web", "message": "Tell me about the legendary fire bird, Moltres."},
    ]

    # Send the welcome message and starters
    await cl.Message(
        content="Hello, Trainer! I'm Pokémon GPT, ready to help you with stats, lore, and strategy.",
        actions=[
            cl.Action(
                name=s["label"],
                payload={"content": s["message"]},
                type="global"
            )
            for s in starters
        ]
    ).send()

    # Initialize history
    cl.user_session.set("message_history", [])

@cl.action_callback
async def on_action(action: cl.Action):
    # Extract the message content the starter should send
    payload = action.payload or {}

    content = payload.get("content")
    if not content:
        return

    # Send the payload as if user typed it
    await cl.Message(content=content).send()

    # Now run it through your main agent
    msg = cl.Message(content="")
    async with agent.run_stream(content) as result:
        async for token in result.stream_text(delta=True, debounce_by=None):
            await msg.stream_token(token)

    await msg.update()

@cl.on_message
async def main(message: cl.Message):


    # Maintain chat history
    # Append the user message to the history list
    history = cl.user_session.get("message_history")
    history.append({"role": "user", "content": message.content})
    cl.user_session.set("message_history", history)

    msg = cl.Message(content="")

    async with agent.run_stream(message.content) as result:
        async for token in result.stream_text(delta=True, debounce_by=None):
            await msg.stream_token(token)

    await msg.update()