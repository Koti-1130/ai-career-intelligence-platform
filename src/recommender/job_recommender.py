import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


def load_data():
    df = pd.read_csv("data/processed/jobs_with_skills.csv")
    return df


def prepare_text(df):
    df["skills_text"] = df["skill_list"].astype(str)
    return df


def recommend_jobs(user_skills, df, top_n=10):

    # Job skill corpus
    job_skills = df["skills_text"].tolist()

    # Create embeddings
    job_embeddings = model.encode(job_skills)

    user_embedding = model.encode([user_skills])

    # Compute similarity
    similarity = cosine_similarity(user_embedding, job_embeddings)

    top_indices = similarity[0].argsort()[-top_n:][::-1]

    recommendations = df.iloc[top_indices][
        ["job_title", "company", "required_skills"]
    ]

    return recommendations.reset_index(drop=True)