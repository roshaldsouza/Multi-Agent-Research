import streamlit as st
from typing import TypedDict
from langgraph.graph import StateGraph, END
from agents.search_agent import search_agent
from agents.summarizer_agent import summarizer_agent
from agents.fact_checker_agent import fact_checker_agent
from agents.report_writer_agent import report_writer_agent

# --- State ---
class ResearchState(TypedDict):
    topic: str
    search_results: str
    summary: str
    fact_check: str
    report: str

# --- Build Graph ---
def build_graph():
    graph = StateGraph(ResearchState)

    graph.add_node("search", search_agent)
    graph.add_node("summarize", summarizer_agent)
    graph.add_node("fact_check", fact_checker_agent)
    graph.add_node("report", report_writer_agent)

    graph.set_entry_point("search")
    graph.add_edge("search", "summarize")
    graph.add_edge("summarize", "fact_check")
    graph.add_edge("fact_check", "report")
    graph.add_edge("report", END)

    return graph.compile()

# --- UI ---
st.set_page_config(page_title="Multi-Agent Research Assistant", page_icon="🔬", layout="wide")

st.title("🔬 Multi-Agent Research Assistant")
st.caption("Powered by Groq + LangGraph + Tavily")

topic = st.text_input(
    "Enter a research topic",
    placeholder="e.g. Impact of AI agents in healthcare 2025"
)

run_button = st.button("🚀 Run Research", type="primary", disabled=not topic)

if run_button and topic:
    app = build_graph()

    progress = st.progress(0, text="Starting pipeline...")
    status = st.empty()

    try:
        with st.spinner("Running agents..."):
            status.info("🔍 Search Agent is gathering information...")
            progress.progress(25, text="Searching the web...")

            result = app.invoke({"topic": topic})

            progress.progress(50, text="Summarizing findings...")
            progress.progress(75, text="Fact checking...")
            progress.progress(100, text="Writing report...")

        progress.empty()
        status.empty()

        st.success("✅ Research complete!")

        st.subheader("🔍 Agent Outputs")

        with st.expander("Search Agent — Raw Results"):
            st.text(result["search_results"])

        with st.expander("Summarizer Agent — Summary"):
            st.write(result["summary"])

        with st.expander("Fact Checker Agent — Fact Check"):
            st.write(result["fact_check"])

        st.divider()
        st.subheader("📄 Final Research Report")
        st.markdown(result["report"])

        st.download_button(
            label="⬇️ Download Report",
            data=result["report"],
            file_name=f"research_{topic[:30].replace(' ', '_')}.md",
            mime="text/markdown"
        )

    except Exception as e:
        progress.empty()
        status.empty()
        st.error(f"❌ Something went wrong: {str(e)}")
        st.info("💡 Check your API keys in the .env file and try again.")