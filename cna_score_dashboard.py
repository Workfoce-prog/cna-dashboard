import streamlit as st
import pandas as pd

# Sample CNA data
data = {
    "Name": ["CNA 1", "CNA 2", "CNA 3"],
    "Tech Adoption": [8, 6, 9],
    "Patient Satisfaction": [9, 8, 9],
    "Documentation Efficiency": [7, 5, 8],
    "Innovation Participation": [6, 4, 8],
    "Training/Upskilling": [9, 6, 10],
    "Teamwork": [9, 7, 10],
    "Time Management": [8, 6, 9],
    "Digital Literacy": [7, 5, 9]
}

weights = {
    "Tech Adoption": 0.10,
    "Patient Satisfaction": 0.25,
    "Documentation Efficiency": 0.10,
    "Innovation Participation": 0.15,
    "Training/Upskilling": 0.10,
    "Teamwork": 0.10,
    "Time Management": 0.10,
    "Digital Literacy": 0.10
}

df = pd.DataFrame(data)

# Calculate weighted scores
def calculate_score(row):
    return sum(row[col] * weights[col] for col in weights)

df["Score"] = df.apply(calculate_score, axis=1)
df["Tier"] = pd.cut(df["Score"], bins=[0, 5, 6, 7, 8.49, 10],
                    labels=["F (At Risk)", "D (Needs Improvement)", "C (Competent)", "B (Very Good)", "A (Excellent)"])

st.title("🩺 CNA Innovation Score Dashboard")
st.dataframe(df)

st.markdown("📊 This dashboard evaluates CNAs using innovation, care, and teamwork metrics.")
