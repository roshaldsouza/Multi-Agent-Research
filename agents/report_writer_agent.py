import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

USE_MOCK = False # Flip to False to test real Groq call

def report_writer_agent(state: dict) -> dict:
    topic = state["topic"]
    summary = state["summary"]
    fact_check = state["fact_check"]

    if USE_MOCK:
        print("📄 [MOCK] Writing final report...")
        mock_report = f"""
# Research Report: {topic}

## Executive Summary
Multi-agent AI systems are rapidly becoming the standard for complex task automation in 2025.
Frameworks like LangGraph and tools like Groq are making these systems faster and more accessible.

## Key Findings
- Multi-agent pipelines are replacing single-model solutions for complex tasks
- LangGraph enables stateful, graph-based orchestration of AI agents
- Groq's LPU hardware makes real-time inference practical and affordable
- Open source models like Llama 3 are competitive for most research tasks

## Fact Check Summary
All major claims were verified against source material.
One claim about open source models was marked partial — true for most but not all tasks.

## Conclusion
The multi-agent AI space is evolving fast. Teams that adopt these patterns now
will have a significant advantage in building robust, scalable AI systems.
        """
        return {"report": mock_report}

    # Real Groq call
    print("📄 [REAL] Writing final report...")
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    prompt = f"""You are an expert research report writer.

Using the summary and fact check report below, write a clean, professional research report in markdown format.

Structure it as:
# Research Report: {topic}

## Executive Summary
(2-3 sentences overview)

## Key Findings
(bullet points of the most important insights)

## Fact Check Summary
(brief note on the reliability of findings based on the fact check)

## Conclusion
(2-3 sentences wrapping up)

---

Summary:
{summary}

Fact Check:
{fact_check}

Write the report now:"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=600,
        temperature=0.4
    )

    report = response.choices[0].message.content.strip()
    return {"report": report}