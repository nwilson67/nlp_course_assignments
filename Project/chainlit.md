# ⚡️ Pokémon GPT Agent: Professor Oak's Research Terminal 🔬

Welcome to the Pokémon GPT Agent! This specialized chatbot is designed to assist both novice and expert trainers by accessing structured data and deep biological lore about the original 151 Pokémon.

## Agent Capabilities

Our Agent uses a sophisticated multi-tool setup to provide accurate, context-aware answers:

1.  **Pokedex SQL Tool (Structured Data):** Accesses a full Pokedex database to retrieve stats, types, and moves. Perfect for factual queries.
    * *Example Queries:* "What is Squirtle's base HP?", "List all moves learned by Pikachu."
2.  **RAG Lore Tool (Unstructured Data):** Uses Retrieval-Augmented Generation to search Professor Oak's research papers. This tool provides biological explanations, capture strategies, and evolutionary details.
    * *Example Queries:* "Why is the Magikarp Paradox significant?", "What is the best way to catch an Abra?", "How does Eevee evolve?"

## How to Interact

The Agent's core intelligence (Gemini) automatically determines the correct tool to use based on your question.

* **For Stats/Moves:** Ask a specific question that requires a numerical or categorical data lookup.
* **For Lore/Strategy:** Ask a conceptual or descriptive question about biology, behavior, or capture methods.

---