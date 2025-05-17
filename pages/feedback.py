import streamlit as st
from utils.gpt_engine import ask_gpt

# Ensure values exist in session
if "current_question" not in st.session_state or "submitted_code" not in st.session_state:
    st.error("Missing session data. Please start from the interview page.")
    st.stop()

company = st.session_state.get("company", "Unknown Company")
interview_type = st.session_state.get("interview_type", "Coding")
question = st.session_state["current_question"]
user_code = st.session_state["submitted_code"]

# Create prompt for GPT
feedback_prompt = f"""
You are a senior software engineer at {company}, conducting a {interview_type} coding round.

Evaluate the candidate's code based on the following question. Provide a JSON response with:
- "feedback": detailed paragraph about correctness, edge cases, readability, performance.
- "score": integer out of 10
- "pass_probability": percentage (0-100)

### Question:
{question}

### Code:
{user_code}

Return ONLY valid JSON.
"""

result = ask_gpt(feedback_prompt, return_json=True)

feedback = result.get("feedback", "No feedback generated.")
score = result.get("score", "N/A")
probability = result.get("pass_probability", "N/A")

left, right = st.columns(2)

with left:
    st.subheader("🧾 Candidate's Code & Question")
    st.markdown("**Question Asked:**")
    st.code(question, language='markdown')
    st.markdown("**Your Code:**")
    st.code(user_code, language='python')

with right:
    st.subheader("✅ AI Interviewer Feedback")
    st.markdown(f"**Score:** {score} / 10")
    st.markdown(f"**Pass Probability:** {probability}%")
    st.markdown("**Feedback:**")
    st.write(feedback)
