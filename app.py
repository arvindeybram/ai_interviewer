import streamlit as st
from streamlit_ace import st_ace
from utils.speech_utils import speak
from utils.db import get_db_connection

st.set_page_config(page_title="AI Mock Interviewer",
                   layout="wide")
st.title("FAANG Taiyyari")

def display_preferences():
    company = st.selectbox("Select Company", ["Meta", "Google", "Microsoft", "Apple"])
    interview_type = st.selectbox("Select Interview Type", ["Coding", "Behavioral"])
    st.markdown("---")
    return company, interview_type


def handle_coding_interview_start(company):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        query = f"""
            SELECT prompt
            FROM questions
            WHERE company_tag = '{company.lower()}'
            ORDER BY RAND() LIMIT 1
        """
        cursor.execute(query)
        question = cursor.fetchone()
        cursor.close()

        if question and question["prompt"]:
            st.session_state.current_question = question["prompt"]
            st.session_state.question_asked = True
            speak("Please read the question and proceed when u, r ready.")
        else:
            st.warning("No questions found for this company.")


def display_coding_question():
    st.markdown("### 💻 Coding Interview Question")
    st.write(st.session_state.current_question)
    st.markdown("### 📝 Your Answer:")
    user_code = st_ace(
        placeholder="Write your code here...",
        language="python",
        theme="monokai",  # Other themes: github, tomorrow_night, etc.
        font_size=18,
        tab_size=4,
        show_gutter=True,
        show_print_margin=False,
        wrap=False,
        min_lines=30,
        max_lines=50,
        height=300,
        auto_update=True,
    )
    return user_code


def handle_answer_submission(company, user_code, interview_type):
    if user_code.strip():
        st.session_state["submitted_code"] = user_code
        st.session_state["company"] = company
        st.session_state["interview_type"] = interview_type
        st.success("✅ Your answer has been submitted.")
        # Manually guide the user to feedback page
        st.markdown("### 👉 [Click here to view your feedback](./pages/feedback.py)")
        st.switch_page("pages/feedback")
    else:
        st.warning("Please enter your code before submitting.")


def handle_reset_question():
    st.session_state.question_asked = False
    st.session_state.current_question = None


def main():
    company, interview_type = display_preferences()

    # Initialize state if not present
    if "question_asked" not in st.session_state:
        st.session_state.question_asked = False
    if "current_question" not in st.session_state:
        st.session_state.current_question = None

    if interview_type == "Coding":
        if not st.session_state.get("question_asked"):
            if st.button("Start Coding Interview"):
                handle_coding_interview_start(company)

        if st.session_state.get("question_asked") and st.session_state.get("current_question"):
            user_code = display_coding_question()
            left_col, right_col = st.columns([1, 1])
            with left_col:
                if st.button("🔄 Reset Question"):
                    handle_reset_question()

            with right_col:
                if st.button("✅ Submit Answer"):
                    handle_answer_submission(company, user_code, interview_type)


if __name__ == "__main__":
    main()
