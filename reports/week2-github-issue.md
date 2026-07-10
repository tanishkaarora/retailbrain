# Week 2 Submission – End-to-End MVP

## ✅ Deliverables

- [x] End-to-end demo
- [x] Updated README
- [x] ADR-001
- [x] At least 10 commits on main
- [x] What surprised me
- [x] Status one-pager

---

## Updated README

The project documentation in `README.md` was thoroughly revised to meet professional project standards:
* **Tech Stack & Architecture:** Clearly outlined the role of Streamlit, LangGraph, Pandas, and FAISS.
* **Installation & Usage:** Added explicit configuration instructions for virtual environments, test runner invocations, and environmental settings.
* **What I Learned:** Added 8 comprehensive engineering takeaways regarding modular design, regex sanitization, semantic routing, and test mock isolation.

---

## ADR-001

Reference:

[docs/adr/ADR-001.md](file:///c:/Users/HP/OneDrive/Desktop/ai%20copilot/docs/adr/ADR-001.md)

**Summary:** We adopted LangGraph StateGraph orchestration to replace a linear pipeline with dynamic query routing. Based on the user's question, an `intent_router` classifies and sends the query to a structured data analytics node (`analytics_node`), an unstructured RAG node (`rag_node`), or a combined execution flow (`both`), preventing prompt context pollution and reducing downstream API token costs.

---

## Commits

The current commit count in the repository is **11 commits** on the main branch.

---

## What Surprised Me

During implementation, I was surprised by how much prompt pollution degraded synthesis quality when quantitative table findings were mixed with unstructured document text. Transitioning to a semantic StateGraph router using LangGraph not only resolved this by separating analytical and retrieval contexts but also drastically optimized API costs by avoiding redundant vector queries.

---

## Status Report

Reference:

[reports/status-week2.md](file:///c:/Users/HP/OneDrive/Desktop/ai%20copilot/reports/status-week2.md)

**Summary:** Week 2 work successfully unified the analytical calculation suite, Plotly chart drawers, and local FAISS vector store into a LangGraph state machine. Standalone tests verify data parsing and mocked routing contexts. Next week's goals include moving to cloud vector storage and splitting the layout into a FastAPI backend and React frontend.
