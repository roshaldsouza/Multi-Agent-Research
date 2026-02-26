import streamlit as st
from typing import TypedDict
from langgraph.graph import StateGraph, END
from agents.search_agent import search_agent
from agents.summarizer_agent import summarizer_agent
from agents.fact_checker_agent import fact_checker_agent
from agents.report_writer_agent import report_writer_agent

# --- State ---
class ResearchState(TypedDict):
    topic: str
    search_results: str
    summary: str
    fact_check: str
    report: str

# --- Page Config ---
st.set_page_config(
    page_title="ResearchOS",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;600&family=Syne:wght@400;600;700;800&display=swap');

*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"] {
    background-color: #080b10 !important;
    color: #c8d6e8 !important;
    font-family: 'JetBrains Mono', monospace !important;
}

[data-testid="stAppViewContainer"] {
    background-image: 
        radial-gradient(ellipse 80% 50% at 50% -20%, rgba(0, 200, 150, 0.07), transparent),
        radial-gradient(ellipse 60% 40% at 80% 80%, rgba(0, 120, 255, 0.05), transparent);
}

[data-testid="stSidebar"] {
    background: #0d1117 !important;
    border-right: 1px solid #1a2332 !important;
}
[data-testid="stSidebar"] * {
    font-family: 'JetBrains Mono', monospace !important;
    color: #8899aa !important;
}
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #e0eaf4 !important;
    font-family: 'Syne', sans-serif !important;
}

#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }
.stDeployButton { display: none; }

h1, h2, h3 { font-family: 'Syne', sans-serif !important; letter-spacing: -0.02em; }

.main-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.8rem;
    font-weight: 800;
    letter-spacing: -0.04em;
    background: linear-gradient(135deg, #00e5a0 0%, #00aaff 60%, #7b61ff 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.1;
    margin-bottom: 0.2rem;
}

.main-subtitle {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    color: #3d5268;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-bottom: 2rem;
}

[data-testid="stTextInput"] input {
    background: #0d1117 !important;
    border: 1px solid #1a2332 !important;
    border-radius: 8px !important;
    color: #c8d6e8 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.9rem !important;
    padding: 0.75rem 1rem !important;
    transition: border-color 0.2s ease !important;
}
[data-testid="stTextInput"] input:focus {
    border-color: #00e5a0 !important;
    box-shadow: 0 0 0 3px rgba(0, 229, 160, 0.08) !important;
}
[data-testid="stTextInput"] label {
    color: #4a6278 !important;
    font-size: 0.7rem !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    font-family: 'JetBrains Mono', monospace !important;
}

[data-testid="stButton"] button {
    background: linear-gradient(135deg, #00e5a0, #00aaff) !important;
    color: #080b10 !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.05em !important;
    padding: 0.6rem 2rem !important;
    transition: opacity 0.2s, transform 0.1s !important;
}
[data-testid="stButton"] button:hover { opacity: 0.9 !important; transform: translateY(-1px) !important; }
[data-testid="stButton"] button:disabled { background: #1a2332 !important; color: #3d5268 !important; }

.agent-card {
    background: #0d1117;
    border: 1px solid #1a2332;
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 1rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.3s ease;
}
.agent-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 3px; height: 100%;
    border-radius: 3px 0 0 3px;
}
.agent-card.search::before   { background: #00e5a0; }
.agent-card.summarize::before { background: #00aaff; }
.agent-card.factcheck::before { background: #f59e0b; }
.agent-card.report::before    { background: #7b61ff; }
.agent-card.active { border-color: #1e3a5f; box-shadow: 0 0 20px rgba(0,170,255,0.06); }

.agent-card-header { display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.75rem; }
.agent-icon { font-size: 1.1rem; width: 2rem; text-align: center; }
.agent-name { font-family: 'Syne', sans-serif; font-weight: 700; font-size: 0.9rem; color: #e0eaf4; flex: 1; }
.agent-status {
    font-size: 0.65rem; letter-spacing: 0.12em; text-transform: uppercase;
    padding: 0.2rem 0.6rem; border-radius: 20px; font-family: 'JetBrains Mono', monospace;
}
.status-waiting { background: #111820; color: #3d5268; border: 1px solid #1a2332; }
.status-running { background: #0a2340; color: #00aaff; border: 1px solid #1a4a7a; animation: pulse 1.5s infinite; }
.status-done    { background: #0a2a1a; color: #00e5a0; border: 1px solid #0d4a2a; }

@keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }

.agent-output {
    font-size: 0.78rem; color: #6a8099; line-height: 1.7;
    border-top: 1px solid #1a2332; padding-top: 0.75rem; margin-top: 0.25rem;
    white-space: pre-wrap; max-height: 160px; overflow-y: auto;
}
.agent-output::-webkit-scrollbar { width: 4px; }
.agent-output::-webkit-scrollbar-track { background: transparent; }
.agent-output::-webkit-scrollbar-thumb { background: #1a2332; border-radius: 2px; }

.report-container {
    background: #0d1117; border: 1px solid #1a2332; border-radius: 12px;
    padding: 2rem; margin-top: 1.5rem; position: relative;
}
.report-container::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, #00e5a0, #00aaff, #7b61ff);
    border-radius: 12px 12px 0 0;
}
.report-label {
    font-family: 'JetBrains Mono', monospace; font-size: 0.65rem;
    letter-spacing: 0.2em; text-transform: uppercase; color: #3d5268; margin-bottom: 1rem;
}

.stat-row { display: flex; gap: 0.75rem; margin-bottom: 1.5rem; flex-wrap: wrap; }
.stat-badge {
    background: #0d1117; border: 1px solid #1a2332; border-radius: 6px;
    padding: 0.4rem 0.75rem; font-size: 0.7rem; color: #4a6278;
    font-family: 'JetBrains Mono', monospace;
}
.stat-badge span { color: #00e5a0; font-weight: 600; }

.history-item {
    background: #0d1117; border: 1px solid #1a2332; border-radius: 8px;
    padding: 0.6rem 0.9rem; margin-bottom: 0.5rem; font-size: 0.72rem; color: #6a8099;
    overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
    transition: border-color 0.2s, color 0.2s;
}

.stMarkdown h1 { color: #e0eaf4 !important; font-size: 1.4rem !important; }
.stMarkdown h2 { color: #c8d6e8 !important; font-size: 1.1rem !important; }
.stMarkdown h3 { color: #a0b4c8 !important; font-size: 0.95rem !important; }
.stMarkdown p, .stMarkdown li { color: #6a8099 !important; font-size: 0.85rem !important; line-height: 1.8 !important; }
.stMarkdown strong { color: #c8d6e8 !important; }

[data-testid="stDownloadButton"] button {
    background: transparent !important; border: 1px solid #1a2332 !important;
    color: #6a8099 !important; font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.75rem !important; border-radius: 6px !important;
    transition: border-color 0.2s, color 0.2s !important;
}
[data-testid="stDownloadButton"] button:hover { border-color: #00e5a0 !important; color: #00e5a0 !important; }
</style>
""", unsafe_allow_html=True)

# === SESSION STATE ===
if "history" not in st.session_state:
    st.session_state.history = []

# === SIDEBAR ===
with st.sidebar:
    st.markdown("### ⬡ ResearchOS")
    st.markdown("<div style='font-size:0.7rem;color:#3d5268;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:1.5rem;'>Multi-Agent Pipeline</div>", unsafe_allow_html=True)

    st.markdown("<div style='font-size:0.7rem;color:#3d5268;letter-spacing:0.12em;text-transform:uppercase;margin-bottom:0.5rem;'>Model</div>", unsafe_allow_html=True)
    model = st.selectbox("", ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768"], label_visibility="collapsed")

    st.markdown("<hr style='border-color:#1a2332;margin:1.25rem 0;'>", unsafe_allow_html=True)

    st.markdown("<div style='font-size:0.7rem;color:#3d5268;letter-spacing:0.12em;text-transform:uppercase;margin-bottom:0.5rem;'>Search Depth</div>", unsafe_allow_html=True)
    search_depth = st.radio("", ["basic", "advanced"], label_visibility="collapsed", horizontal=True)

    st.markdown("<hr style='border-color:#1a2332;margin:1.25rem 0;'>", unsafe_allow_html=True)

    st.markdown("<div style='font-size:0.7rem;color:#3d5268;letter-spacing:0.12em;text-transform:uppercase;margin-bottom:0.75rem;'>Recent Searches</div>", unsafe_allow_html=True)
    if st.session_state.history:
        for item in reversed(st.session_state.history[-6:]):
            st.markdown(f"<div class='history-item'>⬡ {item}</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div style='font-size:0.72rem;color:#2a3f55;font-style:italic;'>No searches yet</div>", unsafe_allow_html=True)

    st.markdown("<hr style='border-color:#1a2332;margin:1.25rem 0;'>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:0.65rem;color:#2a3f55;line-height:1.8;'>Groq · LangGraph · Tavily<br>4 agents · 1 pipeline</div>", unsafe_allow_html=True)

# === MAIN LAYOUT ===
col_main, col_agents = st.columns([1.6, 1], gap="large")

with col_main:
    st.markdown("<div class='main-title'>ResearchOS</div>", unsafe_allow_html=True)
    st.markdown("<div class='main-subtitle'>⬡ Autonomous multi-agent research pipeline</div>", unsafe_allow_html=True)

    topic = st.text_input("RESEARCH TOPIC", placeholder="e.g. Impact of AI agents in healthcare 2025")
    col_btn, _ = st.columns([1, 3])
    with col_btn:
        run_button = st.button("⬡ Run Pipeline", type="primary", disabled=not topic)

    result_area = st.empty()

with col_agents:
    st.markdown("<div style='font-size:0.7rem;color:#3d5268;letter-spacing:0.12em;text-transform:uppercase;margin-bottom:1rem;margin-top:3.8rem;'>Pipeline Status</div>", unsafe_allow_html=True)
    agents_display = st.empty()

    def render_agent_cards(statuses, outputs):
        agents = [
            ("search",    "🔍", "Search Agent",   "Tavily web retrieval"),
            ("summarize", "📝", "Summarizer",      "Groq LLM condensation"),
            ("factcheck", "✅", "Fact Checker",    "Groq claim verification"),
            ("report",    "📄", "Report Writer",   "Groq final synthesis"),
        ]
        html = ""
        for key, icon, name, desc in agents:
            status = statuses.get(key, "waiting")
            output = outputs.get(key, "")
            active_class = "active" if status == "running" else ""
            status_label = {"waiting": "waiting", "running": "running...", "done": "done"}[status]
            output_html = f"<div class='agent-output'>{output[:280]}{'...' if len(output) > 280 else ''}</div>" if output else ""
            html += f"""
            <div class='agent-card {key} {active_class}'>
                <div class='agent-card-header'>
                    <div class='agent-icon'>{icon}</div>
                    <div style='flex:1'>
                        <div class='agent-name'>{name}</div>
                        <div style='font-size:0.65rem;color:#3d5268;'>{desc}</div>
                    </div>
                    <div class='agent-status status-{status}'>{status_label}</div>
                </div>
                {output_html}
            </div>"""
        return html

    agents_display.markdown(render_agent_cards({}, {}), unsafe_allow_html=True)

# === RUN ===
if run_button and topic:
    if topic not in st.session_state.history:
        st.session_state.history.append(topic)

    statuses = {k: "waiting" for k in ["search", "summarize", "factcheck", "report"]}
    outputs = {}
    state = {"topic": topic, "search_results": "", "summary": "", "fact_check": "", "report": ""}

    try:
        # Search
        statuses["search"] = "running"
        agents_display.markdown(render_agent_cards(statuses, outputs), unsafe_allow_html=True)
        r = search_agent(state)
        state.update(r)
        outputs["search"] = r["search_results"]
        statuses["search"] = "done"
        agents_display.markdown(render_agent_cards(statuses, outputs), unsafe_allow_html=True)

        # Summarize
        statuses["summarize"] = "running"
        agents_display.markdown(render_agent_cards(statuses, outputs), unsafe_allow_html=True)
        r = summarizer_agent(state)
        state.update(r)
        outputs["summarize"] = r["summary"]
        statuses["summarize"] = "done"
        agents_display.markdown(render_agent_cards(statuses, outputs), unsafe_allow_html=True)

        # Fact check
        statuses["factcheck"] = "running"
        agents_display.markdown(render_agent_cards(statuses, outputs), unsafe_allow_html=True)
        r = fact_checker_agent(state)
        state.update(r)
        outputs["factcheck"] = r["fact_check"]
        statuses["factcheck"] = "done"
        agents_display.markdown(render_agent_cards(statuses, outputs), unsafe_allow_html=True)

        # Report
        statuses["report"] = "running"
        agents_display.markdown(render_agent_cards(statuses, outputs), unsafe_allow_html=True)
        r = report_writer_agent(state)
        state.update(r)
        outputs["report"] = r["report"]
        statuses["report"] = "done"
        agents_display.markdown(render_agent_cards(statuses, outputs), unsafe_allow_html=True)

        # Show report
        word_count = len(state["report"].split())
        with result_area.container():
            st.markdown(f"""
            <div class='stat-row' style='margin-top:1.5rem;'>
                <div class='stat-badge'>agents <span>4</span></div>
                <div class='stat-badge'>words <span>{word_count}</span></div>
                <div class='stat-badge'>model <span>{model}</span></div>
                <div class='stat-badge'>status <span>complete ✓</span></div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<div class='report-container'>", unsafe_allow_html=True)
            st.markdown("<div class='report-label'>⬡ Final Research Report</div>", unsafe_allow_html=True)
            st.markdown(state["report"])
            st.markdown("</div>", unsafe_allow_html=True)

            st.download_button(
                label="⬇ export as markdown",
                data=state["report"],
                file_name=f"research_{topic[:30].replace(' ', '_')}.md",
                mime="text/markdown"
            )

    except Exception as e:
        agents_display.markdown(render_agent_cards({k: "waiting" for k in statuses}, {}), unsafe_allow_html=True)
        with result_area.container():
            st.error(f"Pipeline error: {str(e)}")
            st.info("💡 Check your API keys in .env and try again.")