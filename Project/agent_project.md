# Agent Project
This project will guide you through building an AI Agent application from beginning to end. You can create an
application for any domain of your choosing, even if it's completely made-up. Feel free to be creative. 
Since our focus is on the application, you are also allowed to make up any data you'd like on the backend.

The assignment is worth 250 points and is due Dec. 5th at 11:59 pm. I should be able to recreate your entire application from beginning to end so 
please include a requirements.txt, documents, scripts to chunk and embed documents, etc. Your application should include the following components:

### RAG Tool [100 points]

Create a separate RAG tool your agent can call. Should include the following:

- At least 10 documents and embedded chunks from those documents [25 points]
  - These can be made-up documents - an LLM can help with this. I don't care how you generate the data so don't worry about including the document generation part in the repo.
  - Make the documents long enough, aim for at least a page or several paragraphs per document. We want chunking to actually do something.
  - For full points, please create a script that shows the process of taking in the documents, chunking them, and finally embedding them. 
  This script should be run offline, storing the documents in an object that is loaded at runtime (you don't want to be embedding documents at runtime).
  Upload the documents to github so I have access to them.
- An appropriate search function (query embedding and functionality that finds the closest chunks). [25 points]
- A reranker [25 points]
- An appropriate LLM and prompt to return results [25 points]


### Database Tool [50 points]

This is a simple tool that takes in a query and returns relevant results from your database. There should be no hard-coded queries.
Make sure to only provide read access to the agent. Points breakdown:

- Tool returns results from db based on query and is read access only [25 points] 
- Include a script that creates the SQLite DB. [25 points]
  - The db should have at least 3 normalized tables containing relevant data to the application, with at least 100 rows on at least one table.
  - Again, you can make this data up.

### Web Search Tool [20 points]

Simple tool that calls the web and returns results. Two options are Exa.ai and Tavily.


### Front-end [50 points]

A Chainlit front-end layer for interacting with the agent. Here are the following elements/features to include:

- A logo [5 points]
- A README describing how to interact with the agent and agent capabilities. [10 points]
- 3 starters to help the user know what to query, one starter for each tool [5 points]
- Streaming of tokens [15 points]
- Maintaining chat history to keep context for the user [15 points]

### Monitoring [10 points]

Set up monitoring via Langfuse and add me as a member.


### Misc. [20 points]

- Please provide 5 test cases I can run and what their outputs should roughly be. 3 points per test case (pass/fail) - [15 points]
- Please add me a PR that is **just** for this project. [5 points]