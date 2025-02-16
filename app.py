import streamlit as st
import pandas as pd
import time
import random
from utils.topic_page import show_topic_page
from utils.document_page import show_document_page
from utils.csv_page import show_csv_page

st.set_page_config(
    page_title="Quiz Station",
    page_icon="📝",
    layout="centered",
    initial_sidebar_state="auto",
)

# Session state initialization
if 'page' not in st.session_state:
    st.session_state.update({
        'page': 'home',
        'quiz_state': 'not_started',
        'current_question': 0,
        'user_answers': {},
        'shuffled_options': {},
        'question_feedback': [],
        'quiz_duration': 0,
        'final_score': 0,
        'quiz_source': None,
        'quiz_df': None,
        'generating': False,
        'start_time': 0
    })

# Sidebar configuration
with st.sidebar:
    st.image("static/quizstation.png")
    st.header("Quiz Configuration")
    quiz_source = st.sidebar.selectbox("Select One", ["Home", "Topic", "Document", "Q&A CSV"], key="quiz_source_select")
    
    if quiz_source != st.session_state.quiz_source:
        st.session_state.quiz_source = quiz_source
        st.session_state.page = quiz_source.lower()
        st.session_state.quiz_df = None
        st.session_state.quiz_state = 'not_started'
        st.session_state.shuffled_options = {}  # ✅ Reset options when switching quiz type
        st.rerun()

# Function to display a question
def display_question():
    idx = st.session_state.current_question
    row = st.session_state.quiz_df.iloc[idx]

    if idx not in st.session_state.shuffled_options:
        options = [row['option1'], row['option2'], row['option3'], row['option4']]
        random.shuffle(options)
        st.session_state.shuffled_options[idx] = options  # ✅ Store new shuffled options

    options = st.session_state.shuffled_options[idx]

    with st.expander(f"Question {idx + 1}", expanded=True):
        st.markdown(f"#### {row['question']}")
        st.session_state.user_answers[idx] = st.radio(
            "Select an answer:", options,
            index=options.index(st.session_state.user_answers[idx]) if idx in st.session_state.user_answers else 0,
            key=f"q{idx}"
        )

# Main content based on current page
if st.session_state.page == 'home':
    st.title("📝 QuizStation")
    st.markdown("""
    ### How to Use QuizStation:
    
    1. **Select Input Method** from the sidebar:
        - **Topic**: Generate quiz from any topic
        - **Document**: Upload a document to create quiz
        - **Q&A CSV**: Upload your own quiz in format
    
    2. **Follow Page Instructions**:
        - Each method has its own dedicated page
        - Fill in required information
        - Click "Get Quizzes" to generate questions
    
    3. **Take the Quiz**:
        - Start quiz when ready
        - Answer all questions
        - Get detailed feedback and scores
    
    Select an input method from the sidebar to begin!
    """)

elif st.session_state.quiz_state == 'not_started':
    if st.session_state.page == 'topic':
        show_topic_page()
        st.session_state.shuffled_options = {}  # ✅ Reset options when new quiz is generated
    elif st.session_state.page == 'document':
        show_document_page()
        st.session_state.shuffled_options = {}  # ✅ Reset options when new quiz is generated
    elif st.session_state.page == 'q&a csv':
        show_csv_page()
        st.session_state.shuffled_options = {}  # ✅ Reset options when new quiz is generated

elif st.session_state.quiz_state == 'in_progress':
    if st.session_state.start_time == 0:
        st.session_state.start_time = time.time()

    st.title("📝 Quiz In Progress")
    # st.dataframe(st.session_state.quiz_df)   # for debugging
    current_q = st.session_state.current_question
    total_q = len(st.session_state.quiz_df)
    st.progress((current_q + 1) / total_q, text=f"Question {current_q + 1} of {total_q}")

    display_question()

    col1, col2 = st.columns([8, 1.2])
    with col1:
        if current_q > 0:
            st.button("Previous", on_click=lambda: st.session_state.update({"current_question": current_q - 1}))
    with col2:    
        if current_q < total_q - 1:
            st.button("Next", on_click=lambda: st.session_state.update({"current_question": current_q + 1}))
        else:
            if st.button("Submit", type="primary"):
                st.session_state.quiz_duration = time.time() - st.session_state.start_time
                st.session_state.quiz_state = 'completed'
                st.rerun()

elif st.session_state.quiz_state == 'completed':
    st.balloons()
    st.title("📊 Quiz Results")

    # Calculate final score and feedback
    score = 0
    feedback = []

    for idx, row in st.session_state.quiz_df.iterrows():
        correct_option = str(row['correct_answer']).strip().lower()
        user_answer = str(st.session_state.user_answers.get(idx, "")).strip().lower()
        is_correct = user_answer == correct_option

        score += int(is_correct)
        feedback.append({
            "Question": row["question"],
            "Your Answer": st.session_state.user_answers.get(idx, ""),
            "Correct Answer": row["correct_answer"],
            "Feedback": "Correct" if is_correct else "Incorrect"
        })

    st.session_state.final_score = score
    st.session_state.question_feedback = feedback

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Final Score", f"{st.session_state.final_score}/{len(st.session_state.quiz_df)}")
    with col2:
        mins = int(st.session_state.quiz_duration // 60)
        secs = int(st.session_state.quiz_duration % 60)
        st.metric("Time Taken", f"{mins}m {secs}s")

    st.subheader("Detailed Feedback")
    feedback_df = pd.DataFrame(st.session_state.question_feedback)

    # Function to format feedback table
    def color_feedback(val):
        if val == "Correct":
            return "background-color: green; color: white"
        elif val == "Incorrect":
            return "background-color: red; color: white"
        return ""

    if not feedback_df.empty:
        styled_feedback = feedback_df.style.applymap(color_feedback, subset=["Feedback"])
        st.dataframe(styled_feedback)
    else:
        st.warning("No feedback available.")

    if st.button("🔄 Take Another Quiz"):
        # Clear all quiz-related session state
        quiz_state_keys = [
            'page', 'quiz_state', 'quiz_df', 'start_time',
            'user_answers', 'current_question', 'shuffled_options'
        ]
        for key in quiz_state_keys:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()