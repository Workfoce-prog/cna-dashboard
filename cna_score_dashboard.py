import streamlit as st
import pandas as pd

st.set_page_config(page_title="CNA Innovation Uploader", layout="centered")
st.title("📤 Upload Your CNA Data for Scoring")

# Description
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

We'll score each CNA and assign a performance tier from A to F.
""")

# Define scoring weights
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

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.success("✅ File uploaded successfully!")

        # Validate columns
        missing_cols = [col for col in weights.keys() if col not in df.columns]
        if missing_cols:
            st.error(f"Missing columns: {', '.join(missing_cols)}")
        else:
            # Calculate score and tier
            df["Score"] = df.apply(lambda row: sum(row[col] * weights[col] for col in weights), axis=1)
            df["Tier"] = pd.cut(
                df["Score"],
                bins=[0, 5, 6, 7, 8.49, 10],
                labels=["F (At Risk)", "D (Needs Improvement)", "C (Competent)", "B (Very Good)", "A (Excellent)"]
            )
            st.subheader("📊 Scored CNA Data")
            st.dataframe(df)

            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Scored Data",
                data=csv,
                file_name="scored_cna_data.csv",
                mime="text/csv"
            )
    except Exception as e:
        st.error(f"❌ Error processing file: {e}")
