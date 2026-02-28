import streamlit as st
import requests
import time
from datetime import datetime

API_BASE = "http://localhost:8000/api"
 
st.set_page_config(
    page_title="Multi-Agent Research System",
    page_icon="🤖",
    layout="wide"
)
 
st.markdown("""
<style>
    .main-title { font-size: 2.5rem; font-weight: 700; color: #1a1a2e; }
    .subtitle   { color: #666; margin-bottom: 2rem; }

    .status-pending   { background:#fff3cd; color:#856404; padding:4px 12px; border-radius:20px; font-size:0.85rem; font-weight:600; }
    .status-running   { background:#cce5ff; color:#004085; padding:4px 12px; border-radius:20px; font-size:0.85rem; font-weight:600; }
    .status-completed { background:#d4edda; color:#155724; padding:4px 12px; border-radius:20px; font-size:0.85rem; font-weight:600; }
    .status-failed    { background:#f8d7da; color:#721c24; padding:4px 12px; border-radius:20px; font-size:0.85rem; font-weight:600; }

    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.2rem; border-radius: 12px; color: white; text-align: center;
    }
    .metric-number { font-size: 2rem; font-weight: 700; }
    .metric-label  { font-size: 0.85rem; opacity: 0.85; }

    .job-card {
        background: white; border: 1px solid #e0e0e0;
        border-radius: 10px; padding: 1rem 1.2rem;
        margin-bottom: 0.6rem;
        box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    }
</style>
""", unsafe_allow_html=True)
 
def status_badge(status: str) -> str:
    icons = {"pending": "⏳", "running": "⚙️", "completed": "✅", "failed": "❌"}
    return f'<span class="status-{status}">{icons.get(status,"")} {status.upper()}</span>'


def fetch_jobs():
    try:
        r = requests.get(f"{API_BASE}/jobs", timeout=5)
        return r.json().get("jobs", []) if r.status_code == 200 else []
    except Exception:
        return None


def fetch_job(job_id: str):
    try:
        r = requests.get(f"{API_BASE}/jobs/{job_id}", timeout=5)
        return r.json() if r.status_code == 200 else None
    except Exception:
        return None


def start_job(topic: str):
    try:
        r = requests.post(f"{API_BASE}/jobs", json={"topic": topic}, timeout=5)
        return r.json() if r.status_code == 201 else None
    except Exception:
        return None


def delete_job(job_id: str):
    try:
        r = requests.delete(f"{API_BASE}/jobs/{job_id}", timeout=5)
        return r.status_code == 204
    except Exception:
        return False


def fmt_time(ts: str) -> str:
    if not ts:
        return "—"
    try:
        return datetime.fromisoformat(ts).strftime("%d %b %Y, %H:%M")
    except Exception:
        return ts

with st.sidebar:
    st.markdown("## 🤖 Multi-Agent Research")
    st.markdown("---")
    page = st.radio("Navigate", ["🏠 Dashboard", "🔬 New Research", "📋 All Jobs", "📖 View Report"])
    st.markdown("---")
 
    try:
        r = requests.get("http://localhost:8000/health", timeout=3)
        if r.status_code == 200:
            st.success("API Online ✅")
        else:
            st.error("API Error ❌")
    except Exception:
        st.error("API Offline ❌")

    st.markdown("---")
    st.caption("Built with CrewAI + Groq + FastAPI")
 
if page == "🏠 Dashboard":
    st.markdown('<p class="main-title">🤖 Research Dashboard</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">AI-powered multi-agent research pipeline</p>', unsafe_allow_html=True)

    jobs = fetch_jobs()

    if jobs is None:
        st.error("❌ Cannot connect to API. Make sure the server is running on port 8000.")
        st.code("uvicorn api.main:app --reload", language="bash")
        st.stop()
 
    total      = len(jobs)
    completed  = sum(1 for j in jobs if j["status"] == "completed")
    running    = sum(1 for j in jobs if j["status"] == "running")
    failed     = sum(1 for j in jobs if j["status"] == "failed")

    c1, c2, c3, c4 = st.columns(4)
    for col, num, label in zip(
        [c1, c2, c3, c4],
        [total, completed, running, failed],
        ["Total Jobs", "Completed", "Running", "Failed"]
    ):
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-number">{num}</div>
                <div class="metric-label">{label}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("### Recent Jobs")
    if not jobs:
        st.info("No research jobs yet. Start one from **🔬 New Research**!")
    else:
        for job in jobs[:8]:
            with st.container():
                st.markdown(f"""
                <div class="job-card">
                    <b>{job['topic']}</b> &nbsp; {status_badge(job['status'])}
                    <br><small style="color:#999">Created: {fmt_time(job['created_at'])}</small>
                </div>""", unsafe_allow_html=True)

elif page == "🔬 New Research":
    st.markdown('<p class="main-title">🔬 Start New Research</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Enter a topic and let the AI agents do the work</p>', unsafe_allow_html=True)

    with st.form("new_job_form"):
        topic = st.text_input(
            "Research Topic",
            placeholder="e.g. Large Language Models in Healthcare 2025",
            max_chars=200
        )
        examples = st.expander("💡 Example topics")
        with examples:
            st.markdown("""
            - AI trends in 2025
            - Future of electric vehicles
            - Quantum computing breakthroughs
            - Generative AI in education
            """)
        submitted = st.form_submit_button("🚀 Start Research", use_container_width=True)

    if submitted:
        if not topic.strip():
            st.warning("Please enter a topic first!")
        else:
            with st.spinner("Starting research job..."):
                job = start_job(topic.strip())

            if job:
                st.success(f"✅ Research job started!")
                st.info(f"**Job ID:** `{job['id']}`\n\nSave this ID to check results in **📋 All Jobs** or **📖 View Report**")
 
                st.markdown("### ⚙️ Live Progress")
                progress_bar = st.progress(0)
                status_text  = st.empty()
                steps = ["Researcher Agent working...", "Writer Agent drafting...",
                         "Critic Agent reviewing...", "Formatter Agent polishing..."]

                for i in range(60):
                    time.sleep(5)
                    current = fetch_job(job["id"])
                    if not current:
                        break

                    pct = min((i + 1) / 60, 0.95)
                    progress_bar.progress(pct)
                    step_label = steps[min(i // 15, 3)]
                    status_text.markdown(f"**Status:** {step_label}  |  `{current['status'].upper()}`")

                    if current["status"] == "completed":
                        progress_bar.progress(1.0)
                        status_text.markdown("**Status:** ✅ Done!")
                        st.balloons()
                        st.success("🎉 Report generated! Go to **📖 View Report** to read it.")
                        st.session_state["last_job_id"] = job["id"]
                        break
                    elif current["status"] == "failed":
                        st.error(f"❌ Job failed: {current.get('error', 'Unknown error')}")
                        break
            else:
                st.error("❌ Failed to start job. Is the API running?")

elif page == "📋 All Jobs":
    st.markdown('<p class="main-title">📋 All Research Jobs</p>', unsafe_allow_html=True)

    col1, col2 = st.columns([6, 1])
    with col2:
        if st.button("🔄 Refresh"):
            st.rerun()

    jobs = fetch_jobs()
    if jobs is None:
        st.error("Cannot connect to API.")
    elif not jobs:
        st.info("No jobs yet.")
    else:
        for job in jobs:
            with st.expander(f"{job['topic']} — {job['status'].upper()}"):
                c1, c2 = st.columns(2)
                c1.markdown(f"**ID:** `{job['id']}`")
                c2.markdown(f"**Created:** {fmt_time(job['created_at'])}")
                st.markdown(status_badge(job["status"]), unsafe_allow_html=True)

                btn_col1, btn_col2 = st.columns(2)
                if job["status"] == "completed":
                    if btn_col1.button("📖 View Report", key=f"view_{job['id']}"):
                        st.session_state["view_job_id"] = job["id"]
                        st.info("Go to **📖 View Report** tab.")
                if btn_col2.button("🗑️ Delete", key=f"del_{job['id']}"):
                    if delete_job(job["id"]):
                        st.success("Deleted!")
                        st.rerun()
 
elif page == "📖 View Report":
    st.markdown('<p class="main-title">📖 View Report</p>', unsafe_allow_html=True)
 
    default_id = st.session_state.get("last_job_id", st.session_state.get("view_job_id", ""))

    job_id = st.text_input("Enter Job ID", value=default_id, placeholder="Paste your job ID here")

    if st.button("🔍 Fetch Report", use_container_width=True) and job_id:
        with st.spinner("Fetching report..."):
            job = fetch_job(job_id.strip())

        if not job:
            st.error("Job not found.")
        elif job["status"] == "pending":
            st.warning("⏳ Job is still pending.")
        elif job["status"] == "running":
            st.info("⚙️ Job is still running. Check back shortly.")
        elif job["status"] == "failed":
            st.error(f"❌ Job failed: {job.get('error', 'Unknown error')}")
        elif job["status"] == "completed":
            st.success(f"✅ Report for: **{job['topic']}**")
            st.markdown("---")
            st.markdown(job["report"])
            st.markdown("---")
            st.download_button(
                label="⬇️ Download Report (.md)",
                data=job["report"],
                file_name=f"{job['topic'][:40].replace(' ','_')}_report.md",
                mime="text/markdown",
                use_container_width=True
            )