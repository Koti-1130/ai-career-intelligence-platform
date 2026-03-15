import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.recommender.job_recommender import load_data

st.set_page_config(
    page_title="AI Career Intelligence Platform",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Career Intelligence Platform")

st.markdown("""
### Make Smarter Career Decisions with Data

The **AI Career Intelligence Platform** helps aspiring AI, data science,
and machine learning professionals explore job opportunities, understand
skill requirements, and analyze job market trends.

This platform analyzes **real job postings** and provides:

• Job recommendations based on your skills  
• Skill gap analysis for your target role  
• Salary insights and job market demand  
• AI skill demand analytics
""")

st.divider()

df = load_data()

st.sidebar.header("Career Profile")

role = st.sidebar.selectbox(
    "Target Role",
    sorted(df["job_title"].unique())
)

skills = st.sidebar.text_input(
    "Your Skills",
    value=st.session_state.get("skills",""),
    placeholder="python, machine learning, aws"
)
st.session_state["skills"] = skills
st.session_state["role"] = role
st.session_state["skills"] = skills

st.success("Your profile is saved. Explore tools in the sidebar.")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Career Explorer")
    st.write("Find jobs matching your current skills.")

with col2:
    st.subheader("Skill Gap Analyzer")
    st.write("Identify the skills needed for your target role.")

with col3:
    st.subheader("Market Insights")
    st.write("Explore demand for AI skills and salary trends.")