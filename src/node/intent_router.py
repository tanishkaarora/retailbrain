"""Routes user questions to the right processing path"""

from src.state.copilot_state import CopilotState
from src.prompts.business_prompts import INTENT_ROUTER_PROMPT

class IntentRouterNode:
    def __init__(self, llm):
        self.llm = llm

    def route(self, state: CopilotState) -> CopilotState:
        """
        Determines whether question needs analytics, RAG, or both.
        This is a cheap LLM call — just classification, no generation.
        """
        # Get context from session (passed via state or config)
        has_csv = bool(state.kpi_summary)    # kpi_summary is set if CSV was uploaded

        prompt = INTENT_ROUTER_PROMPT.format(
            has_csv=str(has_csv),
            has_pdf="yes",
            question=state.question
        )

        response = self.llm.invoke(prompt)
        route_text = response.content.strip().lower()

        # Normalise response
        if "both" in route_text:
            route = "both"
        elif "rag" in route_text:
            route = "rag"
        elif "analytics" in route_text:
            route = "analytics"
        else:
            route = "rag"  # default fallback

        return CopilotState(**{**state.dict(), "route": route})
