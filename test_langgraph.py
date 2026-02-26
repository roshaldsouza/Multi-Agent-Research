from typing import TypedDict
from langgraph.graph import StateGraph, END
from agents.search_agent import search_agent

class ResearchState(TypedDict):
    topic: str
    search_results: str
    summary: str

def summarize_node(state: ResearchState):
    print("📝 Summarizing results...")
    return {"summary": f"Summary placeholder: {state['search_results'][:80]}..."}

graph = StateGraph(ResearchState)

graph.add_node("search", search_agent)       # ← real agent now
graph.add_node("summarize", summarize_node)

graph.set_entry_point("search")
graph.add_edge("search", "summarize")
graph.add_edge("summarize", END)

app = graph.compile()

result = app.invoke({"topic": "Multi-agent AI systems 2025"})

print("\n--- Search Results ---")
print(result["search_results"])