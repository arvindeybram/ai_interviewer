from utils.db import get_db_connection
import streamlit as st
from speech_utils import speak
from gpt_engine import ask_gpt

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
    if not st.session_state.question_asked:
        if st.button("Start Coding Interview"):
            if conn:
                cursor = conn.cursor(dictionary=True)
                query = """
                        SELECT title, difficulty, url 
                        FROM questions 
                        WHERE company_tag = %s 
                        ORDER BY RAND() LIMIT 1
                    """
                cursor.execute(query, (company.lower(),))
                question = cursor.fetchone()
                cursor.close()

                if question:
                    title = question["title"]
                    prompt = ask_gpt(
                        f"""You're a senior software engineer conducting interviews.
                            Take the following LeetCode question title and rephrase it into a full, 
                            clear coding interview question that can be asked aloud. Title: "{title}" """)
                    st.session_state.current_question = {
                        "title": title,
                        "difficulty": question["difficulty"],
                        "url": question["url"],
                        "prompt": prompt
                    }
                    speak(prompt)  # optional
                    st.session_state.question_asked = True
                else:
                    st.warning("No questions found for this company.")
                    conn.close()

                    # Display AI-generated prompt and notepad
                    if st.session_state.question_asked and st.session_state.current_question:
                        q = st.session_state.current_question
                    st.markdown(f"### 💻 Coding Interview Question from {company}")
                    st.write(f"🧠 {q['prompt']}")
                    st.write(f"**Difficulty:** {q['difficulty']}")
                    st.write(f"**URL:** [Click here]({q['url']})")

                    st.markdown("### 📝 Your Answer:")
                    user_code = st.text_area("Write your code here:", height=300)

                    if st.button("Submit Answer"):
                        st.success("✅ Your answer has been submitted.")
