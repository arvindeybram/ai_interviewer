import streamlit as st
from speech_utils import record_audio, transcribe_audio, speak
from gpt_engine import ask_gpt

st.set_page_config(page_title="AI Mock Interviewer", layout="centered")

st.title("🎤 AI Mock Interviewer")
st.markdown("Ask your interview questions via voice. The AI will respond with voice as well.")

if "history" not in st.session_state:
    st.session_state.history = []

duration = 5

if st.button("Start Interview Round"):
    filename = record_audio(duration=duration)
    st.success("Recording complete.")
    with st.spinner("Transcribing..."):
        transcript = transcribe_audio(filename)
    st.write(f"🗣️ You said: `{transcript}`")

    with st.spinner("Thinking..."):
        response = ask_gpt(transcript, st.session_state.history)
    st.write(f"🤖 AI: `{response}`")

    st.session_state.history.append({"user": transcript, "ai": response})

    speak(response)

st.markdown("---")
st.subheader("📝 Interview History")
for i, turn in enumerate(st.session_state.history):
    st.markdown(f"**Q{i+1}:** {turn['user']}")
    st.markdown(f"**A{i+1}:** {turn['ai']}")

