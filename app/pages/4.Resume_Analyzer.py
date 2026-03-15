import streamlit as st
import pdfplumber
import re

st.title("📄 Resume Skill Analyzer")

st.write(
    "Upload your resume and the platform will automatically extract "
    "relevant AI and data skills and add them to your career profile."
)

# -------------------------
# Skill Database
# -------------------------

skills_db = [
    "python","pandas","numpy","sql","spark","hadoop",
    "machine learning","deep learning","nlp","computer vision",
    "pytorch","tensorflow","scikit-learn","xgboost",
    "aws","azure","gcp","docker","kubernetes",
    "tableau","power bi","excel",
    "airflow","dbt","snowflake",
    "transformers","langchain","llm"
]


# -------------------------
# Upload Resume
# -------------------------

uploaded_file = st.file_uploader(
    "Upload your resume (PDF)",
    type=["pdf"]
)

# Save uploaded file in session
if uploaded_file:
    st.session_state["resume_file"] = uploaded_file


# Retrieve stored resume
file = st.session_state.get("resume_file")


# -------------------------
# Function: Extract Text
# -------------------------

def extract_text(file):

    text = ""

    with pdfplumber.open(file) as pdf:

        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text

    return text.lower()


# -------------------------
# Process Resume
# -------------------------

if file:

    st.success(f"Resume Uploaded: {file.name}")

    text = extract_text(file)

    found_skills = []

    for skill in skills_db:

        if re.search(r"\b" + skill + r"\b", text):

            found_skills.append(skill)

    st.subheader("Skills Found in Resume")

    if found_skills:

        for skill in found_skills:

            st.write("✔", skill)

        # Convert skills to comma separated format
        extracted_skills = ", ".join(found_skills)

        # Save to global session profile
        st.session_state["skills"] = extracted_skills

        st.success("Skills automatically added to your career profile!")

    else:

        st.warning("No known skills detected from the resume.")