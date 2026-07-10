# Insight Copilot Demo Guide

This guide outlines the features to be demonstrated, the suggested execution sequence, and the expected outputs for the Week 2 MVP demo.

## Features to Demonstrate

1. **Dual Ingestion (Structured + Unstructured):** Simultaneous processing of CSV/Excel data files and PDF documents.
2. **Dynamic KPI Metrics & Profiling:** Automated calculation of dataset totals, averages, and schema summaries.
3. **Interactive Visualizations:** Generation of dynamic, hover-responsive Plotly charts based on dataset distributions, categories, and timelines.
4. **Context-Aware Intent Routing:** Dynamic query classification (`analytics`, `rag`, or `both`) orchestrating targeted pipeline execution.
5. **Cited Response Synthesis:** Synthesis of statistical tabular data and qualitative page-level citations from document contexts.

---

## Suggested Order of the Demo

### Step 1: Preparation & Setup
* Open the Streamlit application (`streamlit run streamlit_app.py`).
* Point out the clean UI, the header logo, and the instruction checklist on the sidebar.
* Confirm that no data is loaded yet (the UI will show informative info panels under the "Overview", "Charts", and "Ask" tabs).

### Step 2: Tabular Dataset Ingestion
* In the sidebar under **Upload Datasets**, upload a sample retail dataset (CSV or Excel format).
* Click **🚀 Process Files**.
* **Expected Output:** Success banner showing `✅ Data loaded: X rows`.
* Review the **Overview** tab to demonstrate:
  * Dynamic metric cards showing columns like *Total Sales*, *Avg Revenue*, and *Total Rows*.
  * The text-based **Data Profile Summary** detailing columns, row counts, min/max values, and unique counts.

### Step 3: Interactive Dashboards & Plotly Charts
* Click the **Charts** tab.
* **Expected Output:** Auto-generated Plotly plots:
  * **Bar Chart:** Top-N performances (e.g., Sales by Category).
  * **Line Chart:** Trend Over Time (aggregated monthly).
  * **Histogram:** Distribution of the primary numeric column.
  * **Scatter Plot:** Interactive comparisons between numeric variables (colored by category if unique counts are under 15).
* Hover over the bars and lines to show that they are fully interactive.

### Step 4: Qualitative PDF Ingestion
* In the sidebar, upload a business policy or manual PDF under **Business Document**.
* Click **🚀 Process Files**.
* **Expected Output:** Green success cards indicating both the loaded rows and the chunked PDF: `✅ Document indexed: Y chunks`.

### Step 5: Ask Tab — Pure Analytics Routing
* Navigate to the **Ask** tab.
* In the chat input, type an analytical question: e.g., *"Which product has the highest sales?"*
* **Expected Output:**
  * Spinner showing `Analysing...`.
  * The assistant prints a sorted text table of top items.
  * The route caption at the bottom reads: `Route: ANALYTICS | Processing time: Z.Zs`.

### Step 6: Ask Tab — Pure RAG Routing
* In the chat input, type a policy question covered in your PDF: e.g., *"What is the policy for processing customer returns?"*
* **Expected Output:**
  * The assistant responds with text summarizing the rules found in the document.
  * The route caption reads: `Route: RAG`.
  * A clickable **Sources** expander is rendered below the chat response showing the PDF filename (e.g., `• return_policy.pdf p.2`).

### Step 7: Ask Tab — Both (Hybrid) Routing
* In the chat input, type a question that links numbers to policies: e.g., *"Summarize our sales trends and tell me how they align with the marketing strategy guidelines in the strategy document."*
* **Expected Output:**
  * The assistant merges statistics (e.g., growth percentage) with textual directives.
  * The route caption reads: `Route: BOTH`.
  * The **Sources** expander details the page citations.
