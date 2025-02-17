import streamlit as st
import pandas as pd
import google.generativeai as genai
import re

GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")


def clean_question(text):
    """Removes leading numbers, punctuation, and extra quotes from questions."""
    text = text.strip('"')  # Remove leading and trailing quotes
    text = re.sub(r'^\d+[\.\)]?\s*', '', text)  # Remove numbers like "1. ", "2) ", "3 "
    return text

def generate_quiz_from_doc(document_text: str, n: int) -> pd.DataFrame:
    """Generates a quiz based on a given document using Gemini Pro API."""
    
    prompt = (f"Generate {n} quiz questions based on the following document content:\n"
          f"{document_text}\n"
          f"Each question should be formatted exactly as:\n"
          f'"question","option1","option2","option3","option4","correct_answer"\n'
          f"Do not include question numbers, do not prefix numbers to the questions.")
    
    # Generate response using Gemini Pro
    response = model.generate_content(prompt)

    # Debugging: Print raw response
    if response is None:
        st.error("Gemini API returned None.")
        return pd.DataFrame(columns=["question", "option1", "option2", "option3", "option4", "correct_answer"])
    
    if not hasattr(response, "text") or not response.text:
        st.error("Gemini API returned an empty response.")
        return pd.DataFrame(columns=["question", "option1", "option2", "option3", "option4", "correct_answer"])

    response_text = response.text.strip()
    
    # Debugging: Show raw API response in Streamlit
    # with st.expander("🔍 Gemini API Raw Response", expanded=False):
    #     st.text_area("API Output", response_text, height=300)

    quiz_data = []
    for line in response_text.split("\n"):
        columns = [col.strip().strip('"') for col in line.split('","')]
        if len(columns) == 6:
            columns[0] = clean_question(columns[0])  # Remove numbers
            quiz_data.append(columns)
        else:
            st.warning(f"Skipping malformed line: {line}")

    if not quiz_data:
        st.error("No valid quiz questions were extracted. Check API response formatting.")
        return pd.DataFrame(columns=["question", "option1", "option2", "option3", "option4", "correct_answer"])

    df=pd.DataFrame(quiz_data, columns=["question", "option1", "option2", "option3", "option4", "correct_answer"])
 
    df = df[df['question'] != 'question']  # Remove header row
    return df

# doc_to_quiz.py
def load_quiz_from_doc(document_text: str):
    n_questions = st.number_input("Number of questions to generate", min_value=1, value=5)
    quiz_df = generate_quiz_from_doc(document_text, n_questions)
    return quiz_df
