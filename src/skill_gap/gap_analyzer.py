import pandas as pd


def load_data():
    df = pd.read_csv("data/processed/jobs_with_skills.csv")
    return df


def get_job_skills(job_title, df):

    job_row = df[df["job_title"].str.lower() == job_title.lower()]

    if job_row.empty:
        return []

    skills = job_row.iloc[0]["required_skills"]

    job_skills = [skill.strip().lower() for skill in skills.split(",")]

    return job_skills


def analyze_gap(user_skills, job_skills):

    user_set = set([skill.lower().strip() for skill in user_skills])
    job_set = set([skill.lower().strip() for skill in job_skills])

    missing_skills = job_set - user_set

    return list(missing_skills)