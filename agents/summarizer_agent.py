import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

USE_MOCK = False # Flip to False to test real Groq call

def summarizer_agent(state: dict) -> dict:
    search_results = state["search_results"]

    if USE_MOCK:
        print("📝 [MOCK] Summarizing results...")
        mock_summary = """
        Key findings:
        - Multi-agent AI systems are rapidly becoming the standard for complex task automation.
        - Frameworks like LangGraph enable stateful, graph-based agent orchestration.
        - Groq's hardware accelerates inference, making real-time agent pipelines feasible.
        - Open source LLMs are now competitive with proprietary models for most tasks.
        """
        return {"summary": mock_summary}

    # Real Groq call — only when USE_MOCK = False
    print("📝 [REAL] Summarizing results...")
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    prompt = f"""You are a research summarizer.
    
Given the following raw search results, produce a clean and concise summary.
Focus on the most important facts and insights.
Keep it under 150 words.

Search Results:
{search_results}

Summary:"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300,
        temperature=0.3   # lower = more factual, less creative
    )

    summary = response.choices[0].message.content.strip()
    return {"summary": summary}