from typing import TypedDict
from langgraph.graph import StateGraph, END

# 1. Define State — the shared dictionary
class ResearchState(TypedDict):
    topic: str
    search_results: str
    summary: str

# 2. Define Nodes — plain Python functions
def search_node(state: ResearchState):
    print(f"🔍 Searching for: {state['topic']}")
    # Fake search result for now
    return {"search_results": f"Raw results about {state['topic']}: lots of interesting data..."}

def summarize_node(state: ResearchState):
    print(f"📝 Summarizing results...")
    # Fake summary for now
    return {"summary": f"Summary: {state['search_results'][:50]}..."}

# 3. Build the Graph
graph = StateGraph(ResearchState)

graph.add_node("search", search_node)
graph.add_node("summarize", summarize_node)

# 4. Define Edges — the flow
graph.set_entry_point("search")
graph.add_edge("search", "summarize")
graph.add_edge("summarize", END)

# 5. Compile and Run
app = graph.compile()

result = app.invoke({"topic": "Artificial Intelligence trends 2025"})

print("\n--- Final State ---")
print(result)