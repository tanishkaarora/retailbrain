# Week 2 Status

## Objectives

* Implement dynamic query routing to separate structured data calculations from unstructured text inquiries.
* Build automated business analytics helpers for processing sales trends, identifying category performance, and flagging outliers.
* Develop local PDF document parsing, text chunking, and embedding-based indexing via a local vector store.
* Unify frontend dashboard features (metrics, plots) and conversational interfaces in a single web dashboard.
* Verify reliability of the codebase via isolated unit testing.

## Work Completed

* **LangGraph Orchestration:** Replaced a linear pipeline with a `StateGraph` workflow that routes incoming requests to `analytics_node`, `rag_node`, or `both` using an intent classification model.
* **Robust Ingestion Pipeline:** Implemented clean pandas ingestion parsing CSV and Excel sheets, which normalizes column names, converts currency markers ($, £, €, %), handles datetime formats, and cleans duplicate rows.
* **Analytical Analytics Engine:** Designed computations in the `AnalyticsEngine` for top-N ranking, monthly/quarterly trends, and Z-score outlier detection.
* **Plotly Chart Builder:** Created automated visualization code that draws bar charts, timeline trends, histograms, and scatter plots dynamically.
* **Local RAG Integration:** Implemented PDF text extraction, chunking (`RecursiveCharacterTextSplitter`), and local vector search database index using FAISS.
* **Streamlit UI Layout:** Built a dashboard containing a file-upload sidebar, metric grids, auto-rendered charts, and a multi-turn chat widget.
* **Resilient Test Harness:** Configured standalone unit tests verifying ingestion cleaning, and structured mock tests confirming StateGraph routing.

## Challenges

* **State vs. Streamlit Coupling:** Storing large pandas DataFrames in the LangGraph state was causing overhead and memory bloat.
* **Currency Parsing Anomalies:** Ingesting business reports meant dealing with diverse formatting styles like `$1,200.00` or `€50.5%` which crashed standard numeric parsing.
* **Streamlit Script Context in Tests:** Running unit tests on code that interacts with Streamlit generated warnings or errors about missing execution scripts context.

## Solutions

* **Decoupled State Management:** Keep the DataFrame inside the local Streamlit session state while referencing only the metadata, query, and text outputs in the LangGraph `CopilotState`.
* **Regex Cleaning Preprocessors:** Created regex routines to strip currency symbols and trim whitespaces before coercing text fields into numeric vectors.
* **Mock Contexts:** Created clean test-harness mocks for Streamlit session variables inside graph tests to run assertions headlessly.

## Current Progress

The end-to-end MVP is fully functional. Users can upload a retail spreadsheet alongside an unstructured PDF document, view automatically calculated KPIs and Plotly charts, and query the assistant to receive integrated business recommendations. All tests run and pass.

## Next Week Goals

* Split the monolithic layout into a dedicated backend API (FastAPI) and a modern frontend space (React/TypeScript).
* Upgrade from a local FAISS index to a persistent cloud vector database (e.g., pgvector on PostgreSQL).
* Add machine learning models (such as Prophet or XGBoost) to support predictive demand and stock forecasting.

## Reflection (What Surprised Me)

During implementation, I was surprised by how much prompt pollution degraded synthesis quality when quantitative table findings were mixed with unstructured document text. Transitioning to a semantic StateGraph router using LangGraph not only resolved this by separating analytical and retrieval contexts but also drastically optimized API costs by avoiding redundant vector queries.
