import streamlit as st
from utils.speech_utils import speak
from utils.db import get_db_connection

conn = get_db_connection()

st.set_page_config(page_title="AI Mock Interviewer", layout="centered")
st.title("FAANG Taiyyari")

st.markdown("## Select your preferences to begin:")

company = st.selectbox("Select Company", ["Meta", "Google", "Microsoft", "Apple"])
interview_type = st.selectbox("Select Interview Type", ["Coding", "Behavioral"])

st.markdown("---")

# Store state across reruns
if "question_asked" not in st.session_state:
    st.session_state.question_asked = False
if "current_question" not in st.session_state:
    st.session_state.current_question = None

if interview_type == "Coding":
    if not st.session_state.get("question_asked"):
        if st.button("Start Coding Interview"):
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
                    speak("Please read the question and proceed when you are ready.")
                else:
                    st.warning("No questions found for this company.")

    if st.session_state.get("question_asked") and st.session_state.get("current_question"):
        # Show only the prompt
        st.markdown("### 💻 Coding Interview Question")
        st.write(st.session_state.current_question)

        # Text area for the candidate to type their solution
        st.markdown("### 📝 Your Answer:")
        user_code = st.text_area("Write your code here:", height=300)

        if st.button("Reset Question"):
            st.session_state.question_asked = False
            st.session_state.current_question = None

        elif st.button("Submit Answer"):
            st.success("✅ Your answer has been submitted.")
