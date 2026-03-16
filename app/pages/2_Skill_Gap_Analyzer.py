import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import streamlit as st

from src.skill_gap.gap_analyzer import get_job_skills, analyze_gap
from src.recommender.job_recommender import load_data

st.title("📉 Skill Gap Analyzer")

df = load_data()

role = st.session_state.get("role")
skills = st.session_state.get("skills")

st.write("### Target Role:", role)
st.write("### Your Skills:", skills)

if skills:

    user_skills = [s.strip().lower() for s in skills.split(",")]

    job_skills = get_job_skills(role, df)

    gap = analyze_gap(user_skills, job_skills)

    st.subheader("Skills You Should Learn")

    if gap:
        for g in gap:
            st.write("🔹", g)
    else:
        st.success("You already have all required skills!")

else:
    st.info("Enter your skills in the sidebar first.")