from typing import TypedDict
from langgraph.graph import StateGraph, END
from agents.search_agent import search_agent
from agents.summarizer_agent import summarizer_agent
from agents.fact_checker_agent import fact_checker_agent
from agents.report_writer_agent import report_writer_agent

class ResearchState(TypedDict):
    topic: str
    search_results: str
    summary: str
    fact_check: str
    report: str

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

app = graph.compile()

result = app.invoke({"topic": "Multi-agent AI systems 2025"})

print("\n--- FULL PIPELINE RESULTS ---")
print("\n🔍 Search Results:\n", result["search_results"])
print("\n📝 Summary:\n", result["summary"])
print("\n✅ Fact Check:\n", result["fact_check"])
print("\n📄 Final Report:\n", result["report"])