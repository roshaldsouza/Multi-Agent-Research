import os
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()

USE_MOCK = False  # Flip to False only when testing real search

def search_agent(state: dict) -> dict:
    topic = state["topic"]

    if USE_MOCK:
        print(f"🔍 [MOCK] Searching for: {topic}")
        mock_results = """
        1. AI agents are becoming mainstream in 2025, with multi-agent systems leading enterprise adoption.
        2. Groq's LPU architecture is enabling real-time AI inference at unprecedented speeds.
        3. LangGraph is emerging as the go-to framework for building stateful multi-agent pipelines.
        4. Companies are investing heavily in RAG systems for knowledge-grounded AI responses.
        5. Open source models like Llama 3 are closing the gap with proprietary models.
        """
        return {"search_results": mock_results}

    # Real Tavily call — only when USE_MOCK = False
    print(f"🔍 [REAL] Searching for: {topic}")
    client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    
    response = client.search(
        query=topic,
        search_depth="basic",   # use "basic" not "advanced" — saves credits
        max_results=5
    )

    # Extract just the text content from results
    results = "\n".join(
        [f"{i+1}. {r['content']}" for i, r in enumerate(response["results"])]
    )

    return {"search_results": results}