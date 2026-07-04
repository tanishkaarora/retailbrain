"""
New LangGraph workflow for Insight Copilot.
Replaces the old linear Retriever → Responder graph.
"""

from langgraph.graph import StateGraph, END
from src.state.copilot_state import CopilotState
from src.node.intent_router import IntentRouterNode
from src.node.analytics_node import AnalyticsNode
from src.node.synthesiser_node import SynthesiserNode
from src.vectorstore.vectorstore import VectorStore

class CopilotGraphBuilder:

    def __init__(self, llm, vector_store: VectorStore):
        self.llm = llm
        self.vector_store = vector_store
        self.graph = None

        # Initialise nodes
        self.intent_router = IntentRouterNode(llm)
        self.analytics_node = AnalyticsNode(llm)
        self.synthesiser = SynthesiserNode(llm)

    def _rag_node(self, state: CopilotState) -> CopilotState:
        """
        RAG node: retrieves relevant chunks from FAISS, formats as context string.
        Extracted here to avoid a full class for a simple operation.
        """
        try:
            retriever = self.vector_store.get_retriever()
            docs = retriever.invoke(state.question)
            context = "\n\n".join(
                f"[Source: {d.metadata.get('source', 'doc')}, "
                f"Page: {d.metadata.get('page', '?')}]\n{d.page_content}"
                for d in docs[:5]
            )
        except ValueError:
            # Vector store not initialised — no PDF was uploaded
            docs = []
            context = "No documents have been indexed yet."

        return CopilotState(**{**state.dict(), "retrieved_docs": docs, "rag_context": context})

    def _route_edge(self, state: CopilotState) -> str:
        """Conditional edge function — determines which node runs after intent router"""
        return state.route  # "analytics", "rag", or "both"

    def _after_analytics(self, state: CopilotState) -> str:
        """If route is 'both', run RAG after analytics. Otherwise go to synthesiser."""
        if state.route == "both":
            return "rag_node"
        return "synthesiser"

    def build(self):
        builder = StateGraph(CopilotState)

        # Add all nodes
        builder.add_node("intent_router",  self.intent_router.route)
        builder.add_node("analytics_node", self.analytics_node.run)
        builder.add_node("rag_node",        self._rag_node)
        builder.add_node("synthesiser",    self.synthesiser.synthesise)

        # Entry point
        builder.set_entry_point("intent_router")

        # Conditional routing from intent_router
        builder.add_conditional_edges(
            "intent_router",
            self._route_edge,
            {
                "analytics": "analytics_node",
                "rag":       "rag_node",
                "both":      "analytics_node",
                "unknown":   "rag_node",
            }
        )

        # After analytics: if route==both, also run RAG; otherwise synthesise
        builder.add_conditional_edges(
            "analytics_node",
            self._after_analytics,
            {
                "rag_node":    "rag_node",
                "synthesiser": "synthesiser",
            }
        )

        # RAG always goes to synthesiser
        builder.add_edge("rag_node", "synthesiser")

        # Synthesiser → END
        builder.add_edge("synthesiser", END)

        self.graph = builder.compile()
        return self.graph

    def run(self, question: str, chat_history: list = None) -> CopilotState:
        if self.graph is None:
            self.build()
        initial = CopilotState(
            question=question,
            chat_history=chat_history or []
        )
        result = self.graph.invoke(initial)
        return result
