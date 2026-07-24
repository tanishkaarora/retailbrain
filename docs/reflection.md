# Written Reflection — Tanishka Arora — AI Retail Decision Copilot

**Track:** Segment 3 — Applied ML / AI Engineering  
**Project:** AI Retail Decision Copilot (retailbrain)  
**Theme:** Deployed. Documented. Recorded. Reflected.  

---

## Section 1: What I Built

### Project Overview
**RetailBrain** is an AI-powered retail decision copilot designed to bridge the gap between structured business analytics (sales data spreadsheets) and unstructured strategic guidelines (PDF business reports, standard operating procedures, market analyses). Built for store managers and retail business analysts, RetailBrain provides a single, conversational natural-language chat interface that acts as an intelligent assistant. Instead of context-switching between running complex Excel pivot tables and searching through long PDF strategies, users upload their CSV sales logs and PDF policy guidelines and ask natural language questions. The assistant computes accurate statistics (such as category performance, trends, or anomalies) and cross-references them with document clauses, generating unified business briefs containing both numerical calculations and verified document citations.

### Mini-Extension: Smart Column Detective
For my mini-extension, I chose to implement the **Smart Column Detective**. Traditional analytics systems break immediately if user-uploaded CSV files have column names that do not match hardcoded expectations (like "Revenue" vs "total_sales"). To solve this user experience friction, the Smart Column Detective profiles the dataset using a dual-pathway heuristic: first, it checks headers against a regex-based dictionary of standard retail synonyms (e.g. mapping "Sales", "Turnover", or "Earnings" to the target revenue field); second, if rules fail or are low-confidence, it queries the LLM with the dataset's schema profile and sample values to semantically map categoricals, timestamps, and metric fields. I chose to add this extension because data clean-up and column mapping are the single largest points of failure when deploying automated data analysis products to non-technical users, and showing the detective's mapping confidence in the sidebar makes the system transparent and robust.

---

## Section 2: What I Learned About the Tools

Throughout the 4-week development process, I worked intensively with several core libraries and frameworks. Here is my honest assessment of what they actually do, what surprised me, and what I would tell a friend learning them:

1. **LangGraph (Graph Orchestration)**
   * *What it actually does:* It is not an LLM utility; it is a state-machine engine that manages non-linear execution. It maintains a persistent state object across independent execution nodes, allowing conditional routing.
   * *What surprised me:* How challenging state updates can be. Instead of updating session or global variables, you must explicitly return modified dictionary keys from each node to trigger state changes.
   * *Advice to a friend:* Do not treat LangGraph as an LLM router; think of it as a state machine where nodes are pure functions and the transitions are strictly defined by schemas. Keep prompts completely out of the graph orchestration.

2. **FAISS (Local CPU Vector Store)**
   * *What it actually does:* It is a local, in-memory vector similarity index. Unlike high-marketing cloud vector databases (like Pinecone) or server-based databases (like ChromaDB, which frequently runs into Windows C++ compiler installation issues), FAISS runs directly as a pip package.
   * *What surprised me:* Its speed. Even on local CPU with BGE-small embeddings, similarity searches take less than 10 milliseconds.
   * *Advice to a friend:* For single-user prototypes and documents under 50MB, do not waste time setting up Docker containers or cloud API keys for vector databases—FAISS is incredibly lightweight and reliable.

3. **Streamlit (Frontend Dashboard)**
   * *What it actually does:* A frontend engine that renders full-stack web layouts in pure Python.
   * *What surprised me:* Streamlit re-runs the entire script from top to bottom on every user interaction (e.g., clicking a button, typing text), which means any state (like loaded datasets or chat history) is destroyed unless stored in `st.session_state`. Also, its caching decorator `@st.cache_data` requires hashable objects, so passing raw Pandas DataFrames directly into cached functions will crash the app.
   * *Advice to a friend:* Read the Streamlit execution model documentation twice before writing any code, and structure your app around a robust session state manager from the very beginning.

4. **Pandas (Data Manipulation)**
   * *What it actually does:* A high-performance data manipulation library.
   * *What surprised me:* How much better it is to offload calculations to Pandas vector operations instead of letting the LLM read raw data or write code. By writing structured aggregation functions, we ensure 100% mathematical accuracy and save thousands of tokens.
   * *Advice to a friend:* Never trust an LLM to do arithmetic; use the LLM to classify intent and write the final report, but let Pandas do the heavy lifting of calculating numbers.

---

## Section 3: What I Learned About Myself

Building RetailBrain forced me to confront my tendencies as an engineer. What was harder than expected was routing logic debugging and state-management in LangGraph. I spent nearly two days tracking down a bug where the analytics node was not executing because the intent router output had trailing whitespace, preventing route validation. Conversely, what was easier than expected was designing the UI and setting up the Plotly charts—once the structured data was calculated, Streamlit's layouts made rendering beautiful visual components incredibly simple.

I discovered that I absolutely love backend architecture and data pipeline design—specifically, building the Smart Column Detective and writing clean, modular Pandas aggregation logic. There is a deep satisfaction in writing deterministic code that cleanly handles edge cases. On the other hand, I found deploying and managing environment secrets in the cloud to be frustrating, as minor configuration misalignments on the Streamlit Community Cloud server took hours of trial-and-error logs to diagnose.

Regarding time management, I struggled with perfectionism early on. I spent too much time writing extensive utility scripts in Week 1, which put me behind schedule for graph orchestration in Week 2. This procrastination and delay taught me that I need to adopt an iterative, MVP-first mindset. For my 3rd-year projects, I will focus on shipping a bare-bones end-to-end flow in the first few days, and only then add optimizations.

---

## Section 4: What I'd Do Differently

If I were to start the project over, I would decouple the LLM inference provider from the very first day. We relied heavily on Groq Llama 3.1, but when we hit rate limits during automated testing, the lack of a pluggable mock model caused delays. Implementing a robust mock client earlier would have speeded up our CI/CD and test suite. I would also write automated tests *before* writing the Streamlit UI, as debugging graph states is much faster via Pytest command line than by constantly uploading files in a web browser.

I wish my mentor had told me on Day 1: "Do not let Streamlit's simplicity fool you; it is a rapid prototyping tool, not an application framework. Keep your core backend logic entirely independent of Streamlit's libraries." I spent too much time cleaning UI-bound data in the backend, when the data pipeline should have remained a pure python library.

---

## Section 5: What's Next — The 3rd Year Plan

This project represents a strong foundation for my 3rd-year portfolio. By moving away from simple single-prompt chatbot wrappers, I have built a multi-path agent that demonstrates an understanding of engineering trade-offs (e.g., separating structured calculations from unstructured retrieval). 

In the 3rd year, this prototype will serve as the core intelligence engine. I plan to replace the Streamlit frontend with a modern React SPA and migrate the backend to a decoupled FastAPI service. This will allow us to support multi-user authentication, long-term conversation history, and a robust SQL database (like DuckDB) to run complex multi-file joins. It will transition from a standalone helper into a full-scale enterprise analytics platform.
