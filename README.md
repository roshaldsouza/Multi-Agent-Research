# 🔬 Multi-Agent Research Assistant

An AI-powered research pipeline built with **LangGraph**, **Groq**, and **Tavily**.
Give it any topic and it autonomously searches, summarizes, fact-checks, and writes a report.

## 🏗️ Architecture
```
User Input (Topic)
       ↓
 [Search Agent]       ← Tavily web search
       ↓
 [Summarizer Agent]   ← Groq LLM
       ↓
 [Fact Checker Agent] ← Groq LLM
       ↓
 [Report Writer Agent]← Groq LLM
       ↓
 Final Markdown Report
```

## 🤖 Agents

- **Search Agent** — Queries the web via Tavily and returns raw results
- **Summarizer Agent** — Condenses raw results into key findings
- **Fact Checker Agent** — Cross-checks the summary against source material
- **Report Writer Agent** — Produces a structured markdown research report

## 🛠️ Tech Stack

- [Groq](https://groq.com) — Ultra-fast LLM inference (Llama 3.3 70B)
- [LangGraph](https://langchain-ai.github.io/langgraph/) — Multi-agent orchestration
- [Tavily](https://tavily.com) — Real-time web search API
- [Streamlit](https://streamlit.io) — Frontend UI

## 🚀 Run Locally
```bash
git clone https://github.com/yourusername/multi-agent-research
cd multi-agent-research
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file:
```
GROQ_API_KEY=your_groq_key
TAVILY_API_KEY=your_tavily_key
```
```bash
streamlit run app.py
```

## 📁 Project Structure
```
multi-agent-research/
├── app.py
├── agents/
│   ├── search_agent.py
│   ├── summarizer_agent.py
│   ├── fact_checker_agent.py
│   └── report_writer_agent.py
├── requirements.txt
└── .env
```