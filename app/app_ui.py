import streamlit as st
from pathlib import Path
from datetime import datetime

from pdf_reader import read_pdf
from text_splitter import split_text
from ai_engine import ask_llm
from job_analyzer import build_job_prompt
from app_state import save_application, load_applications
from semantic_search import build_index, search
from match_engine import compute_match_score


# -------------------
# PAGE CONFIG
# -------------------
st.set_page_config(
    page_title="CareerPilot AI",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------
# GLOBAL STYLING
# -------------------
st.markdown("""
<style>

/* Background */
.stApp {
    background-color: #0B0F19;
    color: #E5E7EB;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #111827;
}

/* Buttons */
.stButton button {
    background-color: #4F8BF9;
    color: white;
    border-radius: 10px;
    padding: 0.5rem 1rem;
    border: none;
}

/* Expander */
.streamlit-expanderHeader {
    font-weight: 600;
    color: #E5E7EB;
}

/* Metric styling */
[data-testid="stMetricValue"] {
    font-size: 22px;
}

</style>
""", unsafe_allow_html=True)


# -------------------
# HEADER
# -------------------
st.title("🧭 CareerPilot AI")
st.caption("Your AI-powered career copilot")


# -------------------
# LOAD CV
# -------------------
cv_folder = Path("data/cv")
pdf_files = list(cv_folder.glob("*.pdf"))

if not pdf_files:
    st.error("No CV found in data/cv")
    st.stop()

selected_cv = st.selectbox(
    "Select CV",
    pdf_files,
    format_func=lambda x: x.name
)

cv_text = read_pdf(selected_cv)
chunks = split_text(cv_text)
chunk_embeddings = build_index(chunks)


# -------------------
# SIDEBAR DASHBOARD
# -------------------
with st.sidebar:
    st.header("📊 Dashboard")

    apps = load_applications()

    st.metric("Applications", len(apps))

    if apps:
        avg_score = sum([a.get("match_score", 0) or 0 for a in apps]) / len(apps)
        st.metric("Avg Match Score", f"{avg_score:.1f}/100")

    st.markdown("---")

    if st.button("📋 Show Applications"):
        for i, app in enumerate(reversed(apps), start=1):
            with st.expander(f"Application {i}"):
                st.write(f"**Date:** {app.get('date')}")
                st.write(f"**Score:** {app.get('match_score', 'N/A')}")
                st.write(app.get("job_text", "")[:250] + "...")



# -------------------
# MAIN TABS
# -------------------
tab1, tab2 = st.tabs(["CV Intelligence", "Job Analyzer"])


# ===================
# TAB 1: CV INTELLIGENCE
# ===================
with tab1:

    st.subheader("Ask your CV")

    question = st.text_input("Ask a question about your CV")

    if st.button("Generate Answer"):
        if question.strip():

            relevant_chunks = search(question, chunks, chunk_embeddings, top_k=4)
            context = "\n\n".join(relevant_chunks)

            prompt = f"""
You are a precise career assistant.

Use ONLY the context.
If information is missing, say: "not found in CV".

Return structured bullet points.

CONTEXT:
{context}

QUESTION:
{question}
"""

            answer = ask_llm(prompt)

            st.markdown("### Answer")
            st.write(answer)


# ===================
# TAB 2: JOB ANALYZER
# ===================
with tab2:

    st.subheader("Job Analysis & Match Score")

    job_text = st.text_area("Paste job description")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Analyze Job"):
            if job_text.strip():
                result = ask_llm(build_job_prompt(cv_text, job_text))
                st.markdown("### Analysis")
                st.write(result)

    with col2:
        if st.button("Compute Match Score"):
            if job_text.strip():
                score, explanation = compute_match_score(cv_text, job_text)

                st.markdown("### Match Score")
                st.metric("CV Match", f"{score}/100")

                st.progress(score / 100)

                if score > 80:
                    st.success("Strong match")
                elif score > 50:
                    st.warning("Medium match")
                else:
                    st.error("Weak match")

                st.write(explanation)


    st.markdown("---")

    if st.button("Save Application"):
        if job_text.strip():

            score = None
            if "score" in locals():
                score = score

            save_application({
                "date": str(datetime.now()),
                "job_text": job_text,
                "match_score": score
            })

            st.success("Application saved")