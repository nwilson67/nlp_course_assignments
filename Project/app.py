import chainlit as cl
import sqlite3
from dotenv import load_dotenv
from pydantic_ai import Agent, RunContext
from langfuse import get_client
#from tools import get_hogwarts_database_schema, query_hogwarts_database, web_search


def get_pokedex_schema() -> str:

    """
    Returns the schema of the Pokemon database.
    Call this first to understand the table structure before writing queries.
    """
    return """
    The database 'pokedex.db' has 3 tables:

    1. pokemon
       - Columns: pokedex_id (INTEGER PK), name (TEXT), type_1 (TEXT), type_2 (TEXT), base_hp (INTEGER), is_legendary (BOOLEAN)

    2. moves
       - Columns: move_id (INTEGER PK), move_name (TEXT), move_type (TEXT), power (INTEGER), accuracy (INTEGER)

    3. pokemon_moveset (Linking Table)
       - Columns: pokemon_id (FK to pokemon.pokedex_id), move_id (FK to moves.move_id)
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


# def web_search(question:str) -> str:
#     pass
    # exa = Exa(os.get_env("EXA_API_KEY"))


# Load environment variables
load_dotenv()

langfuse = get_client()
Agent.instrument_all()

# Create basic agent
agent = Agent(
    model='google-gla:gemini-2.5-flash-lite',
    system_prompt=("You are Pokemon GPT, a helpful AI chatbot for gamers learning about the original 151 pokemon."
),
tools=[get_pokedex_schema, query_pokedex],
instrument=True)


@cl.on_chat_start
def start_chat():
    # Set message history for the user session when chat is started
    cl.user_session.set("message_history", [])


@cl.on_message
async def main(message: cl.Message):

    # Initialize message object for streaming
    msg = cl.Message(content="")

    async with agent.run_stream(message.content) as result:
        async for token in result.stream_text(delta=True, debounce_by=None):
            await msg.stream_token(token)

    # This essentially sends the final message to the UI and moves on to next turn
    await msg.update()

@agent.tool_plain
def add_numbers(x, y) -> int:
    """Add two numbers and return the result. x is the first number, and y is the second number,"""
    print("using this function")
    return x + y

def rag_tool(query):
    pass
    #1. Load embeddings (pickl or pandas data frame)
    
    #2. Find top 10 embeddings based off query
    #3 Pass top 10 embeddings into reranker
    #4 Pass top (2) documents to LLM