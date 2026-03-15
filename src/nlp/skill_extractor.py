import pandas as pd


def extract_skills(skill_text):

    if pd.isna(skill_text):
        return []

    skill_text = skill_text.lower()

    skills = [skill.strip() for skill in skill_text.split(",")]

    return skills


def process_skills(input_path, output_path):

    df = pd.read_csv(input_path)

    print("Dataset loaded:", df.shape)

    df["skill_list"] = df["required_skills"].apply(extract_skills)

    df.to_csv(output_path, index=False)

    print("Skill extraction completed")


if __name__ == "__main__":

    input_path = "data/raw/job_postings.csv"
    output_path = "data/processed/jobs_with_skills.csv"

    process_skills(input_path, output_path)