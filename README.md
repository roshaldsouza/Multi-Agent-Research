# 🔬 Multi-Agent Research Assistant

> An autonomous AI research pipeline that searches, summarizes, fact-checks, and writes reports — powered by **LangGraph**, **Groq**, and **Tavily**.

[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)](https://python.org)
[![LangGraph](https://img.shields.io/badge/LangGraph-latest-purple)](https://langchain-ai.github.io/langgraph/)
[![Groq](https://img.shields.io/badge/Groq-Llama%203.3%2070B-orange)](https://groq.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-UI-red?logo=streamlit)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-green)](LICENSE)

---

## 📖 Overview

Give it a topic — get back a structured research report in seconds.

The pipeline autonomously dispatches a team of specialized AI agents: one scours the web for fresh data, another distills it into key findings, a third validates the facts, and a final agent compiles everything into a clean, readable markdown report. No manual prompting required between steps.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    User Input (Topic)                    │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │    🔍 Search Agent    │  ← Tavily real-time web search
              └──────────┬───────────┘
                         │  raw search results
                         ▼
              ┌──────────────────────┐
              │  📝 Summarizer Agent  │  ← Groq LLM (Llama 3.3 70B)
              └──────────┬───────────┘
                         │  key findings
                         ▼
              ┌──────────────────────┐
              │ ✅ Fact Checker Agent │  ← Groq LLM (Llama 3.3 70B)
              └──────────┬───────────┘
                         │  verified summary
                         ▼
              ┌──────────────────────┐
              │ 📄 Report Writer Agent│  ← Groq LLM (Llama 3.3 70B)
              └──────────┬───────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │  Final Markdown Report│
              └──────────────────────┘
```

---

## 🤖 Agent Breakdown

| Agent | Role | Powered By |
|-------|------|------------|
| **Search Agent** | Queries the web and retrieves raw, up-to-date results for the given topic | Tavily Search API |
| **Summarizer Agent** | Condenses raw results into structured key findings, filtering noise | Groq / Llama 3.3 70B |
| **Fact Checker Agent** | Cross-references the summary against original sources, flags inconsistencies | Groq / Llama 3.3 70B |
| **Report Writer Agent** | Compiles verified findings into a well-structured markdown research report | Groq / Llama 3.3 70B |

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| [**Groq**](https://groq.com) | Ultra-fast LLM inference via Llama 3.3 70B — handles summarization, fact-checking, and report writing |
| [**LangGraph**](https://langchain-ai.github.io/langgraph/) | Stateful multi-agent orchestration with directed graph execution |
| [**Tavily**](https://tavily.com) | Real-time web search API optimized for LLM pipelines |
| [**Streamlit**](https://streamlit.io) | Lightweight frontend for topic input and report display |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- A [Groq API key](https://console.groq.com)
- A [Tavily API key](https://app.tavily.com)

### Installation

```bash
# 1. Clone the repo
git clone https://github.com/yourusername/multi-agent-research
cd multi-agent-research

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate       # macOS/Linux
# venv\Scripts\activate        # Windows

# 3. Install dependencies
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_key_here
TAVILY_API_KEY=your_tavily_key_here
```

### Run

```bash
streamlit run app.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser, enter a topic, and let the agents do the work.

---

## 📁 Project Structure

```
multi-agent-research/
│
├── app.py                        # Streamlit entry point
│
├── agents/
│   ├── search_agent.py           # Tavily web search integration
│   ├── summarizer_agent.py       # Key findings extraction
│   ├── fact_checker_agent.py     # Source cross-referencing
│   └── report_writer_agent.py    # Final markdown report generation
│
├── requirements.txt              # Python dependencies
└── .env                          # API keys (not committed)
```

---

## 💡 Example Output

**Input:** `"Latest developments in fusion energy 2024"`

**Output:** A structured markdown report covering recent breakthroughs, key players, technical progress, and open challenges — with facts verified against the original sources.

---

## 🔧 Configuration & Customization

- **Swap the LLM**: Replace Groq with any LangChain-compatible model (OpenAI, Anthropic, etc.) by updating the agent files.
- **Adjust search depth**: Modify the number of Tavily results in `search_agent.py` to trade off speed vs. coverage.
- **Extend the pipeline**: Add new agents (e.g., a citation formatter or bias detector) by inserting nodes into the LangGraph graph.

---

## 🤝 Contributing

Contributions are welcome! Please open an issue to discuss what you'd like to change, or submit a pull request directly for bug fixes.

---

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
