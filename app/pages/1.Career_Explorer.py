import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import streamlit as st
from src.recommender.job_recommender import recommend_jobs, load_data, prepare_text

st.title("💼 Career Explorer")

st.write(
    "Discover job opportunities based on your current skills and target role."
)

# -----------------------
# Load Dataset
# -----------------------

df = load_data()
df = prepare_text(df)

role = st.session_state.get("role")
skills = st.session_state.get("skills")

st.write("### Target Role:", role)
st.write("### Your Skills:", skills)

# -----------------------
# Filters
# -----------------------

st.subheader("Job Filters")

col1, col2, col3 = st.columns(3)

with col1:
    remote_filter = st.selectbox(
        "Remote Preference",
        ["All", "Remote Only"]
    )

with col2:
    min_salary = st.slider(
        "Minimum Salary",
        50000,
        250000,
        80000,
        step=5000
    )

with col3:
    companies = ["All"] + sorted(df["company"].unique().tolist())

    company_filter = st.selectbox(
        "Company",
        companies
    )

# -----------------------
# Job Recommendation
# -----------------------

if skills:

    filtered_df = df[df["job_title"].str.contains(role, case=False, na=False)]

    if filtered_df.empty:
        filtered_df = df

    # Apply filters

    if remote_filter == "Remote Only":
        filtered_df = filtered_df[filtered_df["remote"] == True]

    filtered_df = filtered_df[filtered_df["salary_usd"] >= min_salary]

    if company_filter != "All":
        filtered_df = filtered_df[filtered_df["company"] == company_filter]

    if filtered_df.empty:
        st.warning("No jobs match your filters.")
    else:

        top_n = st.slider("Number of job recommendations", 5, 20, 10)

        recommendations = recommend_jobs(skills, filtered_df, top_n)

        recommendations = recommendations.reset_index(drop=True)

        st.subheader("Recommended Jobs")

        for i, row in recommendations.iterrows():

            job_row = filtered_df[
                (filtered_df["job_title"] == row["job_title"]) &
                (filtered_df["company"] == row["company"])
            ].iloc[0]

            with st.container():

                st.markdown(f"### {row['job_title']}")

                col1, col2 = st.columns(2)

                with col1:
                    st.write("**Company:**", row["company"])

                    if "location" in job_row:
                        st.write("**Location:**", job_row["location"])

                with col2:
                    if "salary_usd" in job_row:
                        st.write(f"**Salary:** ${int(job_row['salary_usd']):,}")

                    if "remote" in job_row:
                        st.write("**Remote:**", job_row["remote"])

                st.write("**Required Skills:**", row["required_skills"])

                with st.expander("View Job Description"):

                    if "description" in job_row:
                        st.write(job_row["description"])

                    st.button("Apply", key=f"apply_{i}")

                st.divider()

else:
    st.info("Enter your skills in the sidebar to see job recommendations.")