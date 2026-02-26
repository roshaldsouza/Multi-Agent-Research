import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

USE_MOCK = True  # Flip to False to test real Groq call

def fact_checker_agent(state: dict) -> dict:
    summary = state["summary"]
    search_results = state["search_results"]

    if USE_MOCK:
        print("✅ [MOCK] Fact checking summary...")
        mock_fact_check = """
        Fact Check Report:
        - ✅ Claim about multi-agent systems is supported by search results.
        - ✅ LangGraph mention is accurate and well supported.
        - ✅ Groq's speed advantage is confirmed by multiple sources.
        - ⚠️  "Open source models competitive with proprietary" is partially supported — true for some tasks, not all.
        """
        return {"fact_check": mock_fact_check}

    # Real Groq call
    print("✅ [REAL] Fact checking summary...")
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    prompt = f"""You are a strict fact checker.

You will be given:
1. A summary written by an AI
2. The original source material it was based on

Your job is to verify each claim in the summary against the source material.
For each claim mark it as:
- ✅ Supported — clearly backed by the sources
- ⚠️  Partial — only somewhat supported or lacks detail
- ❌ Unsupported — not found in the sources at all

Be concise. List each finding on a new line.

Summary:
{summary}

Original Source Material:
{search_results}

Fact Check Report:"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=400,
        temperature=0.1  # very low — we want strict, consistent checking
    )

    fact_check = response.choices[0].message.content.strip()
    return {"fact_check": fact_check}