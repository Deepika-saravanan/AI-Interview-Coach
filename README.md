# 🎤 AI Interview Coach using Streamlit and Hugging Face

An **AI-powered interview simulation platform** that helps users **practice technical interviews** by analyzing their resumes and generating **personalized interview questions**.  
The model listens to the user’s **spoken answers**, evaluates grammar and relevance, and provides **AI-driven feedback and scoring**.

---

## 🔧 Features

- Upload your **resume (PDF)** and get **personalized interview questions**.
- **Dynamic question generation** using **Hugging Face API**.
- **Speech-to-text** transcription using **Whisper** and `ffmpeg`.
- **Answer evaluation** with grammar correction and scoring.
- **Interactive Streamlit web interface** for smooth user experience.
- **Session management** for multiple interview rounds.
- **Safe key management** using `.env` file.

---

## 🎨 Demo

![AI Interview Coach Screenshot](images\img1.png)

---

## 🚀 Installation & Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/Deepika-saravanan/AI-Interview-Coach.git
   cd AI-Interview-Coach
  ```

2. **Create a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # (macOS/Linux)
   venv\Scripts\activate     # (Windows PowerShell)
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your Hugging Face API key**

   ```bash
   HUGGINGFACE_API_KEY=your_api_key_here
   ```
   
5. **Run the app**

   ```bash
   streamlit run app.py
   ```

   Access at `http://localhost:8501` 

---

## 📝 Usage

Upload your resume (PDF).

The model extracts your skills and experience.
It generates 10 unique questions based on your resume.
Answer each question by uploading or recording audio.

The model:
Converts speech to text 🗣️
Corrects grammar ✍️
Evaluates accuracy and relevance 🧠
Gives you a final score and feedback 🎯

---

## ⚙️ How It Works

```text
The system uses multiple AI components integrated via Streamlit:

1. Resume Parser:
   Extracts text and technical skills from the uploaded resume.
2. Question Generator:
   Uses Hugging Face API (Mistral-7B-Instruct) to create custom, resume-specific questions.
3. Speech-to-Text:
   Converts user's audio answers into text using Whisper.
4. Evaluator:
   Analyzes grammar, fluency, and answer relevance using language models.
5. Feedback System:
   Scores and provides constructive feedback for improvement.

```

---

## 🔒 Security Notes
- Do not push your .env file or API keys to GitHub.
-.gitignore already excludes .env, .venv/, and data folders.
-Keep API keys private for security and rate-limit protection.

🧑‍💻 Developed by: Deepika Saravanan
