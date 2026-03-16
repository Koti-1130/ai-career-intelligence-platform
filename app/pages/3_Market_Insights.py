import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import streamlit as st
import pandas as pd
import plotly.express as px

from src.recommender.job_recommender import load_data


st.title("📊 Market Insights")

df = load_data()

role = st.session_state.get("role")

st.write(f"### Market Insights for: {role}")

filtered_df = df[df["job_title"].str.contains(role, case=False, na=False)]

if filtered_df.empty:
    filtered_df = df


# --------------------------------------------------
# Top Skills Demand
# --------------------------------------------------

st.subheader("🔥 Most In-Demand Skills")

skills = filtered_df["required_skills"].str.split(",")

skill_list = []

for group in skills:
    for skill in group:
        skill_list.append(skill.strip().lower())

skill_df = pd.DataFrame(skill_list, columns=["skill"])

top_skills = skill_df["skill"].value_counts().head(10).reset_index()

top_skills.columns = ["skill","count"]

fig_skills = px.bar(
    top_skills,
    x="skill",
    y="count",
    title=f"Top Skills Required for {role} Jobs",
)

st.plotly_chart(fig_skills, use_container_width=True)


# --------------------------------------------------
# Salary Insights
# --------------------------------------------------

if "salary_usd" in filtered_df.columns:

    st.subheader("💰 Salary Insights")

    avg_salary = int(filtered_df["salary_usd"].mean())
    min_salary = int(filtered_df["salary_usd"].min())
    max_salary = int(filtered_df["salary_usd"].max())

    col1, col2, col3 = st.columns(3)

    col1.metric("Average Salary", f"${avg_salary:,}")
    col2.metric("Lowest Salary", f"${min_salary:,}")
    col3.metric("Highest Salary", f"${max_salary:,}")


    # Salary Distribution (Box Plot)

    st.subheader("Salary Distribution")

    fig_salary = px.box(
        filtered_df,
        y="salary_usd",
        points="all",
        title=f"Salary Distribution for {role}"
    )

    st.plotly_chart(fig_salary, use_container_width=True)


# Salary Range Breakdown

st.subheader("Salary Range Breakdown")

bins = [80000,100000,120000,140000,160000,180000,200000,250000]

filtered_df["salary_range"] = pd.cut(
    filtered_df["salary_usd"],
    bins=bins
).astype(str)

salary_ranges = (
    filtered_df["salary_range"]
    .value_counts()
    .sort_index()
    .reset_index()
)

salary_ranges.columns = ["range","count"]

fig_ranges = px.bar(
    salary_ranges,
    x="range",
    y="count",
    title="Number of Jobs in Each Salary Range"
)

st.plotly_chart(fig_ranges, use_container_width=True)


# --------------------------------------------------
# Remote vs Onsite Jobs
# --------------------------------------------------

if "remote" in filtered_df.columns:

    st.subheader("🌍 Remote vs Onsite Jobs")

    remote_counts = filtered_df["remote"].value_counts().reset_index()

    remote_counts.columns = ["remote","count"]

    fig_remote = px.pie(
        remote_counts,
        names="remote",
        values="count",
        title="Remote vs Onsite Distribution"
    )

    st.plotly_chart(fig_remote, use_container_width=True)
    # --------------------------------------------------
# Top Hiring Companies
# --------------------------------------------------

st.subheader("🏢 Top Hiring Companies")

top_companies = (
    filtered_df["company"]
    .value_counts()
    .head(10)
    .reset_index()
)

top_companies.columns = ["company", "count"]

fig_companies = px.bar(
    top_companies,
    x="company",
    y="count",
    title=f"Top Companies Hiring for {role}"
)

st.plotly_chart(fig_companies, use_container_width=True)