#Used to create embeddings offline
import pandas as pd
import pickle
import numpy as np
from dotenv import load_dotenv
from voyageai.client import Client
from typing import List, Tuple

# --- Configuration ---
DOCS_FILENAME = "pokemon_docs.csv"
VECTOR_STORE_FILENAME = "pokemon_vector_store_paragraph.pkl"

# --- RAG Tool Initialization ---
load_dotenv()
try:
    # Initialize Voyage Client once outside the main loop
    VOYAGE_CLIENT = Client(api_key="---")
except Exception as e:
    print(f"Error initializing Voyage AI Client: {e}. Check VOYAGE_API_KEY environment variable.")
    VOYAGE_CLIENT = None


# Chunking function
def paragraph_splitter(text: str) -> List[str]:
    """Splits text into chunks based on paragraph breaks."""

    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    if not paragraphs and '\n' in text:
        paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
    return paragraphs


# --- Embedding Function (Takes a list, returns a list) ---
def batch_embed_chunks(chunks: List[str]) -> List[np.ndarray]:
    """
    Takes a list of all chunks and returns a list of embeddings using Voyage AI.
    """
    if not VOYAGE_CLIENT:
        print("Cannot embed, VOYAGE_CLIENT is not initialized.")
        return []

    print(f"\n   Calling Voyage AI to embed {len(chunks)} chunks in one batch...")

    response = VOYAGE_CLIENT.embed(
        chunks,
        model="voyage-3.5",
        input_type="document"
    )

    # Convert list of embeddings to a list of NumPy arrays
    embeddings = [np.array(e) for e in response.embeddings]

    return embeddings


# --- Main Preparation Logic (Correctly batches the embedding) ---
def prepare_store():
    print(f"--- 1. Loading documents from {DOCS_FILENAME} ---")
    try:
        df = pd.read_csv(DOCS_FILENAME)
    except FileNotFoundError:
        print(f"Error: Document file '{DOCS_FILENAME}' not found.")
        return

    # 1. Collect all chunk texts from all documents
    all_chunks_text: List[str] = []

    print("--- 2. Collecting and Chunking All Documents by Paragraph ---")

    for index, row in df.iterrows():
        content = row['body']
        chunks = paragraph_splitter(content)
        all_chunks_text.extend(chunks)

    print(f"Total paragraphs/chunks collected: {len(all_chunks_text)}")

    # 3. Embed ALL chunks in a single batch call
    all_embeddings = batch_embed_chunks(all_chunks_text)

    if len(all_chunks_text) != len(all_embeddings):
        print("Error: Mismatch between chunk count and embedding count. Aborting.")
        return

    # 4. Create the final vector store structure: [(chunk_text, embedding_vector), ...]
    vector_store: List[Tuple[str, np.ndarray]] = list(zip(all_chunks_text, all_embeddings))

    print(f"\nSuccessfully created and embedded {len(vector_store)} total chunks.")

    # 5. Save the vector store offline
    with open(VECTOR_STORE_FILENAME, 'wb') as f:
        pickle.dump(vector_store, f)

    print(f"--- 6. Vector store successfully saved to {VECTOR_STORE_FILENAME} ---")


if __name__ == "__main__":
    prepare_store()