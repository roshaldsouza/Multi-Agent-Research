from typing import TypedDict
from langgraph.graph import StateGraph, END
from agents.search_agent import search_agent
from agents.summarizer_agent import summarizer_agent
from agents.fact_checker_agent import fact_checker_agent

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

graph.set_entry_point("search")
graph.add_edge("search", "summarize")
graph.add_edge("summarize", "fact_check")
graph.add_edge("fact_check", END)

app = graph.compile()

result = app.invoke({"topic": "Multi-agent AI systems 2025"})

print("\n--- Summary ---")
print(result["summary"])

print("\n--- Fact Check ---")
print(result["fact_check"])