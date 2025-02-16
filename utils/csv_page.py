import streamlit as st
from utils.csv_to_quiz import load_quiz_from_csv

def show_csv_page():
    st.title("📊 Upload Q&A CSV")

    # Information Section
    with st.expander("ℹ️ How to Use, Technology & Cautions", expanded=False):
        st.markdown("""
        ### How to Use:
        1. Upload a **CSV file** containing Q&A pairs.
        2. The file should follow the required format (see below).
        3. If the CSV is valid, you can start the quiz.

        ### Required CSV Format:
        Your CSV should contain the following columns:
        ```
        question, option1, option2, option3, option4, correct_answer
        ```
        - Each row represents a **multiple-choice question**.
        - Ensure that **correct_answer** matches one of the four options.

        ### Technologies Used:
        - **Streamlit** for the UI.
        - **Pandas** for reading and handling CSV files.
        - **Python CSV Handling** for parsing and loading data.

        ### Cautions:
        - The **CSV format must be correct**; otherwise, quiz loading will fail.
        - Ensure **no empty values** in the required columns.
        - Large CSV files may take longer to process.
        """)

    # File Upload Section
    uploaded_file = st.file_uploader("Upload Q&A CSV file:", type=["csv"])

    if uploaded_file:
        try:
            df = load_quiz_from_csv(uploaded_file)
            if df is not None and not df.empty:
                st.session_state.quiz_df = df
                st.success("Quiz loaded successfully!")
                
                if st.button("Start Quiz"):
                    st.session_state.quiz_state = "in_progress"
                    st.rerun()  # Force a rerun to apply the state update immediately
            else:
                st.error("Failed to load quiz. Please check CSV format.")
        except Exception as e:
            st.error(f"Error loading quiz: {str(e)}")