"""Runs analytics operations on the business DataFrame"""

from src.state.copilot_state import CopilotState
from src.analytics.analytics_engine import AnalyticsEngine
import streamlit as st

class AnalyticsNode:
    def __init__(self, llm):
        self.llm = llm
        self.engine = AnalyticsEngine()

    def run(self, state: CopilotState) -> CopilotState:
        """
        Determines what analytics to run based on question keywords,
        runs the computation, and stores result in state.
        """
        # Get the DataFrame from Streamlit session state
        # (passed externally because DataFrames can't be in LangGraph state)
        df = st.session_state.get("clean_df")
        profile = st.session_state.get("data_profile")

        if df is None or profile is None:
            analytics_result = "No data file has been uploaded. Please upload a CSV or Excel file first."
        else:
            analytics_result = self._run_analysis(state.question, df, profile)

        return CopilotState(**{**state.model_dump(), "analytics_result": analytics_result})

    def _run_analysis(self, question: str, df, profile: dict) -> str:
        """Select and run the right analytics based on question content"""
        q = question.lower()
        nums = profile["numeric_cols"]
        cats = profile["cat_cols"]
        dates = profile["date_cols"]

        results = []

        # Top/bottom performers
        if any(w in q for w in ["top", "best", "highest", "most"]):
            if cats and nums:
                results.append(self.engine.top_n_by_column(df, cats[0], nums[0], ascending=False))

        if any(w in q for w in ["bottom", "worst", "lowest", "underperform"]):
            if cats and nums:
                results.append(self.engine.top_n_by_column(df, cats[0], nums[0], ascending=True))

        # Trend
        if any(w in q for w in ["trend", "over time", "monthly", "growth", "decline", "drop"]):
            if dates and nums:
                results.append(self.engine.trend_over_time(df, dates[0], nums[0]))

        # Anomalies
        if any(w in q for w in ["anomaly", "anomalies", "unusual", "spike", "outlier"]):
            if nums:
                results.append(self.engine.detect_anomalies(df, nums[0], cats[0] if cats else None))

        # Default: full summary
        if not results:
            results.append(self.engine.full_summary(df, profile))

        return "\n\n".join(results)
