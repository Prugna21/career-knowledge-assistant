import streamlit as st
from pathlib import Path
from datetime import datetime
import uuid

from pdf_reader import read_pdf
from text_splitter import split_text
from ai_engine import ask_llm
from job_analyzer import build_job_prompt
from app_state import (
    save_application,
    load_applications,
    delete_application,
    update_application
)
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
# STYLE
# -------------------
st.markdown("""
<style>

.stApp {
    background-color: #0B0F19;
    color: #E5E7EB;
}

section[data-testid="stSidebar"] {
    background-color: #111827;
}

.stButton button {
    background-color: #4F8BF9;
    color: white;
    border-radius: 10px;
    padding: 0.5rem 1rem;
    border: none;
}

.streamlit-expanderHeader {
    font-weight: 600;
    color: #E5E7EB;
}

</style>
""", unsafe_allow_html=True)


# -------------------
# HEADER
# -------------------
st.title("🧭 CareerPilot AI")
st.caption("AI-powered career assistant")


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

@st.cache_resource
def prepare_cv(cv_text):
    chunks = split_text(cv_text)
    embeddings = build_index(chunks)
    return chunks, embeddings

chunks, chunk_embeddings = prepare_cv(cv_text)


# -------------------
# SIDEBAR
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
        apps = load_applications()

        if not apps:
            st.info("No applications saved yet.")
        else:
            for i, app in enumerate(reversed(apps), start=1):
                app_id = app.get("id")

                with st.expander(f"Application {i} | Score: {app.get('match_score', 'N/A')}"):
                    st.write(app.get("date"))
                    st.write(app.get("job_text", ""))

                    if app_id:
                        if st.button("🗑️ Delete", key=f"del_{app_id}"):
                            delete_application(app_id)
                            st.rerun()

# -------------------
# TABS
# -------------------
tab1, tab2 = st.tabs(["CV Intelligence", "Job Analyzer"])


# ===================
# TAB 1
# ===================
with tab1:

    st.subheader("Ask about your CV")

    question = st.text_input("Ask a question about your CV")

    if st.button("Generate Answer"):
        if question.strip():

            relevant_chunks = search(question, chunks, chunk_embeddings, top_k=4)
            context = "\n\n".join(relevant_chunks)

            prompt = f"""
You are a precise career assistant.

Use ONLY the context.
If information is missing say: "not found in CV".

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
# TAB 2
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

                st.session_state["last_score"] = score
                st.session_state["last_job"] = job_text

                st.markdown("### Match Score")
                score = score or 0
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

            save_application({
                "id": str(uuid.uuid4()),
                "date": str(datetime.now()),
                "job_text": job_text,
                "match_score": st.session_state.get("last_score")
            })

            st.success("Application saved")