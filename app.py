import streamlit as st
import sys, os, tempfile
sys.path.append(".")
from backend.parser import extract_text
from backend.extractor import extract_all, extract_skills
from backend.matcher import match
from backend.scorer import calculate_score
from backend.suggester import get_suggestions

st.set_page_config(page_title="AI Resume Analyser", page_icon="📄", layout="wide")

st.markdown("""
    <h1 style='text-align:center; color:#4F46E5;'>📄 AI Resume Analyser</h1>
    <p style='text-align:center; color:gray;'>Upload your resume & paste a job description to get your ATS score + AI suggestions</p>
    <hr>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.subheader("📁 Upload Your Resume")
    uploaded_file = st.file_uploader("PDF or DOCX", type=["pdf", "docx"])

with col2:
    st.subheader("📋 Paste Job Description")
    jd_text = st.text_area("Job Description", height=200,
                            placeholder="Paste the job description here...")

if st.button("🚀 Analyse Resume", use_container_width=True):
    if not uploaded_file:
        st.warning("Please upload your resume.")
    elif not jd_text.strip():
        st.warning("Please paste a job description.")
    else:
        with st.spinner("Analysing your resume..."):

            # Save uploaded file temporarily
            suffix = ".pdf" if uploaded_file.name.endswith(".pdf") else ".docx"
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                tmp.write(uploaded_file.read())
                tmp_path = tmp.name

            # Run pipeline
            resume_text = extract_text(tmp_path)
            resume_data = extract_all(resume_text)
            jd_skills   = extract_skills(jd_text)
            match_result = match(resume_text, jd_text, resume_data["skills"], jd_skills)
            score = calculate_score(
                match_result["semantic_score"],
                match_result["skill_match"]["match_percent"],
                resume_data["sections"]
            )
            suggestions = get_suggestions(
                resume_text, jd_text,
                score["final_score"],
                match_result["skill_match"]["missing"]
            )
            os.unlink(tmp_path)

        st.success("Analysis complete!")
        st.markdown("---")

        # Score section
        st.subheader("📊 ATS Score Report")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("🤖 Semantic Match", f"{score['semantic_score']}/100")
        c2.metric("🛠️ Skill Match",    f"{score['skill_match']}%")
        c3.metric("📋 Completeness",   f"{score['completeness']}%")
        c4.metric("⭐ Final Score",    f"{score['final_score']}/100")

        grade_color = {"Excellent":"🟢","Good":"🔵","Average":"🟡","Needs Work":"🔴"}
        st.markdown(f"### Grade: {grade_color.get(score['grade'],'⚪')} {score['grade']}")

        st.markdown("---")

        # Skills section
        col3, col4 = st.columns(2)
        with col3:
            st.subheader("✅ Matched Skills")
            for skill in match_result["skill_match"]["matched"]:
                st.success(skill)

        with col4:
            st.subheader("❌ Missing Skills")
            if match_result["skill_match"]["missing"]:
                for skill in match_result["skill_match"]["missing"]:
                    st.error(skill)
            else:
                st.info("No missing skills!")

        st.markdown("---")

        # Resume info
        st.subheader("👤 Extracted Resume Info")
        st.write(f"**Name:** {resume_data['name']}")
        st.write(f"**Email:** {resume_data['contact']['email']}")
        st.write(f"**Phone:** {resume_data['contact']['phone']}")

        st.markdown("---")

        # AI suggestions
        st.subheader("💡 AI-Powered Suggestions")
        st.markdown(suggestions)