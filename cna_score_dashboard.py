import streamlit as st
import pandas as pd

st.set_page_config(page_title="CNA Innovation Uploader", layout="centered")
st.title("📤 Upload Your CNA Data for Scoring")

st.markdown("""
Upload your own CNA performance data (CSV format) with the following columns:

- Name
- Tech Adoption
- Patient Satisfaction
- Documentation Efficiency
- Innovation Participation
- Training/Upskilling
- Teamwork
- Time Management
- Digital Literacy

If no file is uploaded, sample CNA data will be shown automatically.
""")

# Define weights
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

# File uploader
uploaded_file = st.file_uploader("Choose your CNA data CSV file", type=["csv"])

# Load data: from file or sample
if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.success("✅ File uploaded successfully!")
    except Exception as e:
        st.error(f"❌ Error processing file: {e}")
        df = None
else:
    st.info("ℹ️ No file uploaded. Displaying sample CNA data.")
    df = pd.DataFrame({
        "Name": ["CNA 1", "CNA 2", "CNA 3"],
        "Tech Adoption": [8, 6, 9],
        "Patient Satisfaction": [9, 8, 9],
        "Documentation Efficiency": [7, 5, 8],
        "Innovation Participation": [6, 4, 8],
        "Training/Upskilling": [9, 6, 10],
        "Teamwork": [9, 7, 10],
        "Time Management": [8, 6, 9],
        "Digital Literacy": [7, 5, 9]
    })

# Proceed if valid data
if df is not None:
    # Ensure required columns are present
    missing_cols = [col for col in weights if col not in df.columns]
    if missing_cols:
        st.error(f"Missing required columns: {', '.join(missing_cols)}")
    else:
        # Score calculation
        df["Score"] = df.apply(lambda row: sum(row[col] * weights[col] for col in weights), axis=1)
        df["Tier"] = pd.cut(
            df["Score"],
            bins=[0, 5, 6, 7, 8.49, 10],
            labels=["F (At Risk)", "D (Needs Improvement)", "C (Competent)", "B (Very Good)", "A (Excellent)"]
        )

        st.subheader("📊 CNA Innovation Scorecard")
        st.dataframe(df)

        # Download scored data
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Scored Data",
            data=csv,
            file_name="scored_cna_data.csv",
            mime="text/csv"
        )
