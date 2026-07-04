# Design Document: AI Retail Decision Copilot

## 1. Project Overview
The **AI Retail Decision Copilot** is a state-of-the-art decision-support system designed to empower retail store managers, business analysts, and executives with automated, conversational insights. By fusing structured business analytics (sales, inventory, customers) with unstructured document retrieval (business reports, market manuals) and advanced predictive forecasting, the platform simplifies complex data-driven decision-making. 

The application utilizes a multi-agentic or graph-driven design powered by **LangGraph**, orchestrating structured Python data processing pipelines and a **Retrieval-Augmented Generation (RAG)** pipeline. The end user interacts with a unified conversational agent that automatically routes queries, performs computations, retrieves semantic document contexts, and synthesizes unified business answers with visualizations.

---

## 2. Problem Statement
Modern retail operations generate a vast amount of data across disparate silos:
* **Structured Data:** Transaction databases, inventory logs, and customer sheets (often stored as CSV or Excel sheets).
* **Unstructured Data:** Market research, supplier contracts, standard operating procedures, and business reports (often PDFs).

Retail decision-makers face three primary challenges:
1. **Technical Barriers:** Extracting insights from structured data requires SQL, Python, or complex BI dashboard setups (e.g., Tableau/PowerBI).
2. **Context Fragmentation:** Answering a simple question like *"Why are sales dropping?"* requires correlating numeric sales data with text-heavy business reports.
3. **Reactive vs. Proactive Planning:** Standard analytics engines show historical facts, but do not provide autonomous demand forecasting or actionable step-by-step recommendations.

The **AI Retail Decision Copilot** addresses these gaps by offering a unified, natural language chat interface that acts as an intelligent colleague capable of both calculating metrics and reading operational documents.

---

## 3. Objectives
* **Democratize Retail Analytics:** Allow non-technical managers to query databases using natural language.
* **Bridge Structured and Unstructured Contexts:** Build a graph-based workflow that combines statistical data summaries with RAG-retrieved semantic clauses.
* **Automate Insight Generation:** Identify top/bottom performers, seasonal trends, and data anomalies without manual configuration.
* **Provide Actionable Recommendations:** Synthesize raw figures and documents into logical business responses.
* **Ensure Modular Scalability:** Develop a codebase structured around independent modules (Analytics, Ingestion, Vector DB, Chat Routing) that can scale into a 3rd-year production-grade platform.

---

## 4. Functional Requirements

### 4.1 CSV/Excel Upload & Data Profiling
* **Multi-file Ingestion:** Support uploading separate files for Sales, Inventory, and Customers.
* **Automatic Parsing:** Detect column names, identify data types (numeric, categorical, temporal), clean missing values, and standardize currency strings to floats.
* **Dynamic Dataset Profiling:** Generate an internal metadata schema (keys, columns, statistics) to guide LLM-based analytics routing.

### 4.2 PDF Upload & Ingestion (RAG)
* **Document Processing:** Parse multi-page PDF documents, extract text, and chunk it using character-overlap parameters.
* **Vector Store Ingestion:** Generate dense semantic embeddings of document chunks and insert them into a local vector database.

### 4.3 Automated Business Analytics
* **Category Analysis:** Identify best/worst performing products, categories, or regions.
* **Trend Analysis:** Compute sales growth, decline, and monthly or quarterly trends.
* **Anomaly Detection:** Identify statistical outliers (e.g., unexpected spikes or drops in stock levels/revenues) and display visual warnings.
* **Interactive Charting:** Automatically generate interactive Plotly charts matching the context of the user's analytical query.

### 4.4 RAG Engine & Document QA
* **Semantic Retrieval:** Retrieve relevant document excerpts based on user question similarity.
* **Verification and Citations:** Append document source names and page numbers to claims generated from unstructured text.

### 4.5 AI Chat Routing & Synthesis
* **Intent Routing:** Route the question dynamically. Determine whether it requires structured database analytics, document retrieval (RAG), or a joint synthesis of both.
* **Business Synthesis:** Format raw statistical figures and textual document clauses into a concise, professional executive answer.

---

## 5. Non-Functional Requirements

### 5.1 Scalability
* **Stateless Workflow Nodes:** Ensure LangGraph nodes pass state data explicitly via state objects, allowing easy scaling to serverless execution environments.
* **Interchangeable Models:** Decouple LLM client code via standard abstractions to support switching between OpenAI, Gemini, and Groq models.

### 5.2 Maintainability
* **Clean Code Architecture:** Separate business logic (`src/analytics/`) from graph orchestration (`src/graph_builder/`) and the user interface (`streamlit_app.py`).
* **Pydantic Validation:** Enforce strict type validation across state transitions using Pydantic schemas.

### 5.3 Security
* **Secure Key Management:** Avoid hardcoded keys; manage credentials using secure environment files (`.env`), Streamlit secrets, or transient session states.
* **Data Privacy:** Prevent persistent caching of uploaded spreadsheets or PDFs on external servers. All processing runs in the memory space of the host machine.

### 5.4 Performance
* **In-Memory Querying:** Leverage Pandas vector operations for low-latency calculations.
* **Vector Chunk Optimization:** Utilize FAISS local indexing for sub-second semantic search response times.

### 5.5 Modularity
* **Decoupled Nodes:** Ensure each LangGraph node functions as a standalone micro-operation that can be isolated, unit tested, or reused.

---

## 6. Target Users
* **Store Managers:** Need instant stock-level alerts, item replenishment timelines, and daily sales performance summaries.
* **Business Analysts:** Require quick segment comparisons, sales trend analysis, and raw visual chart generation.
* **Retail Executives:** Request consolidated high-level reports merging regional sales statistics with written policy changes or audit reports.

---

## 7. Technology Stack

| Layer | Component / Tool | Rationale |
| :--- | :--- | :--- |
| **User Interface** | Streamlit | Rapid prototyping of highly interactive, data-rich dashboards and real-time chat widgets in pure Python. |
| **Graph Orchestration** | LangGraph | State-machine approach allowing loops, conditional branch routing, and strict state schemas during AI workflows. |
| **LLM Interface** | LangChain / LangChain Community | Unified API wrapper over multiple model providers (OpenAI, Google Gemini, Groq). |
| **Embeddings & Vector Store** | HuggingFace Embeddings & FAISS | High-performance, memory-efficient local semantic indexing without cloud vendor dependencies. |
| **Data Manipulation** | Pandas & NumPy | Standard, optimized tools for dataset cleaning, profiling, aggregation, and mathematical calculation. |
| **Visualizations** | Plotly | Dynamic, interactive charts that can be rendered directly inside the Streamlit web layout. |
| **Testing** | Pytest | Native Python testing framework for validating analytics code correctness and state transformations. |
| **Configuration** | Python-dotenv | Clean environment variable loading for API secrets separation. |

---

## 8. Project Scope

### Phase 1: Local Prototype (Current Version)
* Unified single-user Streamlit application.
* Local FAISS database in-memory.
* Automated keyword-based analytics routing + basic RAG retrieval.
* Core LangGraph state machine with 4 distinct nodes.

### Phase 2: Web API & Frontend Separation (3rd Year Upgrade)
* Migrate Streamlit UI to a modern React-based Single Page Application.
* Build a decoupled backend API service using FastAPI.
* Transition to a persistent cloud vector database (e.g., Pinecone or pgvector).
* Expand unstructured parsing to support Excel, Word, and text files.

### Phase 3: Collaborative Multi-Agent & Predictive Platform
* Integrate Machine Learning forecasting (using Scikit-Learn or Prophet) for future demand prediction.
* Support multi-agent architecture (e.g., autonomous Inventory Agent, Pricing Optimization Agent).
* Deploy multi-tenant user authentication, database persistence, and history tracking.

---

## 9. Risks and Mitigations

| Risk | Impact | Mitigation Strategy |
| :--- | :--- | :--- |
| **LLM Hallucinations** | High | Ground all synthesiser responses in actual analytics outputs and exact RAG semantic citations. Avoid open-ended generation. |
| **CSV Memory Contraints** | Medium | Implement data limits (e.g., warning prompts when uploaded files exceed 100,000 rows) and process datasets using efficient chunking if necessary. |
| **API Costs & Rate Limits** | Medium | Offer easy switching to free model alternatives (e.g., Groq Llama-3, local Hugging Face pipelines) and minimize token usage by routing simple queries dynamically. |
| **Data Exposure** | High | Do not store uploaded user files persistently; keep processing transient in the local runtime container. |

---

## 10. Future Scope
* **Predictive Stock Replenishment:** Introduce automated machine learning forecasting to predict which SKU units will run out of stock in the upcoming 30 days.
* **Voice-Enabled Assistant:** Integrate speech-to-text capabilities for hands-free warehouse queries.
* **Automated Weekly Email Briefings:** Schedule background tasks that auto-generate executive summary PDF reports and email them to stakeholders.
