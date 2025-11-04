import streamlit as st
import os
import warnings
from modules.resume_parser import extract_text_from_resume
from modules.question_generator import generate_questions_from_resume
from modules.speech_to_text import convert_audio_to_text
from modules.evaluator import evaluate_answer

# Suppress warnings for cleaner output
warnings.filterwarnings("ignore")
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Paths
UPLOAD_DIR = "data/resumes"
AUDIO_DIR = "data/answers"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(AUDIO_DIR, exist_ok=True)

# Streamlit setup
st.set_page_config(page_title="AI Interview Coach", page_icon="🎤", layout="centered")
st.title("🎤 AI Interview Coach")
st.write("Upload your resume and practice your interview with AI!")

# Session state initialization
if "current_question" not in st.session_state:
    st.session_state.current_question = 0
    st.session_state.questions = []
    st.session_state.score_total = 0
    st.session_state.num_answered = 0

# Step 1: Upload Resume
uploaded_resume = st.file_uploader("📄 Upload your Resume (PDF only)", type=["pdf"])

if uploaded_resume:
    resume_path = os.path.join(UPLOAD_DIR, uploaded_resume.name)
    with open(resume_path, "wb") as f:
        f.write(uploaded_resume.getbuffer())

    with st.spinner("📖 Reading your resume..."):
        resume_text = extract_text_from_resume(resume_path)

    st.success("✅ Resume uploaded and text extracted successfully!")

    # Step 2: Generate Questions based on resume content
    if st.button("🧠 Generate Interview Questions"):
        with st.spinner("Generating personalized questions... please wait ⏳"):
            questions = generate_questions_from_resume(resume_text)
            if questions:
                st.session_state.questions = questions
                st.session_state.current_question = 0
                st.session_state.score_total = 0
                st.session_state.num_answered = 0
                st.success("✅ Questions generated successfully!")
            else:
                st.error("❌ Failed to generate questions. Please try again.")

# Step 3: Display and answer questions
# Step 3: Display and answer questions
if st.session_state.questions:
    current_question_index = st.session_state.current_question
    question = st.session_state.questions[current_question_index]
    st.markdown(f"### Q{current_question_index + 1}: {question}")

    # Upload new audio for this question
    uploaded_audio = st.file_uploader(
        "🎙️ Upload your voice answer (WAV/MP3)", 
        type=["wav", "mp3"], 
        key=f"audio_{current_question_index}"  # unique key for each question
    )

    if uploaded_audio:
        audio_path = os.path.join(AUDIO_DIR, f"q{current_question_index+1}_{uploaded_audio.name}")
        with open(audio_path, "wb") as f:
            f.write(uploaded_audio.getbuffer())

        with st.spinner("🎧 Transcribing your answer..."):
            try:
                text_answer = convert_audio_to_text(audio_path)
            except Exception as e:
                text_answer = ""
                st.error(f"Error during transcription: {e}")

        if text_answer.strip():
            with st.spinner("🧩 Evaluating your answer..."):
                feedback = evaluate_answer(question, text_answer)

            st.success("✅ Evaluation Complete")
            st.write("**Your Answer:**", feedback["original"])
            st.write("**Corrected Answer:**", feedback["corrected"])
            st.write(f"**Grammar Score:** {feedback['grammar_score']} / 10")
            st.write(f"**Relevance Score:** {feedback['relevance_score']} / 10")
            st.write(f"**Final Score:** {feedback['final_score']} / 10")
            st.info(feedback["feedback"])

            # Update score
            st.session_state.score_total += feedback["grammar_score"]
            st.session_state.num_answered += 1

            # ✅ Only enable Next Question after evaluation
            if st.session_state.current_question < len(st.session_state.questions) - 1:
                if st.button("Next Question ➡️"):
                    # Clear old data
                    st.session_state.current_question += 1
                    st.session_state.pop(f"audio_{current_question_index}", None)
                    st.rerun()
            else:
                st.success("🎉 Interview Completed!")
                avg_score = round(st.session_state.score_total / st.session_state.num_answered, 2)
                st.write(f"**Your Average Score:** {avg_score}/10")
        else:
            st.warning("⚠️ Could not transcribe your audio clearly. Please upload again.")