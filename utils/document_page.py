import streamlit as st
import pymupdf
from utils.doc_to_quiz import load_quiz_from_doc

def show_document_page():
    st.title("📄 Generate Quiz from Document")

    # Information Section
    with st.expander("ℹ️ How to Use, Technology & Cautions", expanded=False):
        st.markdown("""
        ### How to Use:
        1. Upload a **PDF** or **TXT** file.
        2. Click **"Get Quizzes"** to extract text and generate quiz questions.
        3. The extracted text will be previewed before quiz generation.
        4. If successful, a **"Start Quiz"** button will appear.

        ### Technologies Used:
        - **Streamlit** for the UI.
        - **PyMuPDF (Fitz)** for extracting text from PDFs.
        - **Gemini Pro API** for quiz generation.
        - **Pandas** for handling quiz data.

        ### Cautions:
        - Ensure the uploaded file is **readable** (scanned PDFs may not work).
        - The quiz quality depends on the extracted text.
        - If extraction fails, try a different document format.
        - Large files might take longer to process.
        """)

    # File Upload Section
    uploaded_file = st.file_uploader("Upload document (PDF/TXT):", type=["pdf", "txt"])

    if uploaded_file and st.button("Get Quizzes"):
        with st.spinner("Processing document and generating quiz..."):
            st.session_state.generating = True
            doc = pymupdf.open(stream=uploaded_file.read(), filetype="pdf")
            document_text = "\n".join(page.get_text() for page in doc)
            with st.expander("🔍 Extracted Text Preview", expanded=False):
                st.text_area("Document Content", document_text, height=300)
            try:
                df = load_quiz_from_doc(document_text)
                if df is not None and (not df.empty):
                    st.session_state.quiz_df = df
                    st.success("Quiz generated successfully!")
                    st.button("Start Quiz", type="primary", 
                             on_click=lambda: st.session_state.update({"quiz_state": "in_progress"}))
                else:
                    st.error("Failed to generate quiz. Please try again.")
            except Exception as e:
                st.error(f"Error generating quiz: {str(e)}")
            finally:
                st.session_state.generating = False
