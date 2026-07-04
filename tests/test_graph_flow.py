import sys
import os
from pathlib import Path
import pytest

# Add src to python path
sys.path.append(str(Path(__file__).parent.parent))

from src.state.copilot_state import CopilotState
from src.graph_builder.graph_builder import CopilotGraphBuilder
from src.vectorstore.vectorstore import VectorStore

class MockLLMResponse:
    def __init__(self, content: str):
        self.content = content

class MockLLM:
    def __init__(self, response_text: str):
        self.response_text = response_text
        self.calls = []

    def invoke(self, prompt: str):
        self.calls.append(prompt)
        return MockLLMResponse(self.response_text)

class MockVectorStore(VectorStore):
    def __init__(self):
        self.embeddings = None
        self.db = None
    def get_retriever(self):
        class MockRetriever:
            def invoke(self, question):
                from langchain_core.documents import Document
                return [Document(page_content="Mock doc content", metadata={"source": "test.pdf", "page": 1})]
        return MockRetriever()

def test_graph_analytics_route():
    llm = MockLLM("analytics")
    vs = MockVectorStore()
    builder = CopilotGraphBuilder(llm=llm, vector_store=vs)
    graph = builder.build()
    
    # We run the graph. The intent router will return "analytics".
    # Since we mocked the LLM to return "analytics", it should route to the analytics node,
    # and then to the synthesiser node.
    # We will need the synthesiser LLM invocation to return a business response.
    
    # Let's override the LLM's response for the synthesizer:
    # Actually, we can use a stateful mock LLM
    class StatefulMockLLM:
        def __init__(self):
            self.calls = []
        def invoke(self, prompt):
            self.calls.append(prompt)
            if "classifying" in prompt.lower() or "intent" in prompt.lower():
                return MockLLMResponse("analytics")
            else:
                return MockLLMResponse("This is a synthesized analytics answer.")
                
    stateful_llm = StatefulMockLLM()
    builder = CopilotGraphBuilder(llm=stateful_llm, vector_store=vs)
    
    # Let's mock the Streamlit session state for data frame
    import streamlit as st
    st.session_state["clean_df"] = None
    st.session_state["data_profile"] = None
    
    result = builder.run(question="What is the sales trend?")
    
    # Assert result structure and contents
    assert result["route"] == "analytics"
    assert "No data file has been uploaded" in result["analytics_result"]
    assert result["answer"] == "This is a synthesized analytics answer."
    print("test_graph_analytics_route passed!")

if __name__ == "__main__":
    test_graph_analytics_route()
