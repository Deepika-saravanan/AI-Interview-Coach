import requests
import os
import random

# Hugging Face API setup
HF_API_KEY = os.getenv("HUGGINGFACE_API_KEY")  # Make sure you set this in your .env file
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"

headers = {"Authorization": f"Bearer {HF_API_KEY}"}


def generate_interview_questions(skills, resume_text="", num_questions=10):
    """
    Generate AI-based interview questions dynamically based on extracted skills and resume.
    """

    # Combine all details into a single context
    prompt = f"""
    You are an AI interview coach. Read the following resume content and skills, 
    then generate {num_questions} unique and professional technical interview questions.

    Resume Content: {resume_text[:2000]}  # limit to 2000 chars for efficiency
    Key Skills: {', '.join(skills)}

    Each question should be:
    - Relevant to the resume and skills
    - Technical and professional (like for a job interview)
    - Clear and short (one sentence)
    - Different from each other
    """

    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 500, "temperature": 0.7}
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        result = response.json()

        if isinstance(result, list):
            output_text = result[0].get("generated_text", "")
        else:
            output_text = result.get("generated_text", "")

        # Split into individual questions
        questions = [q.strip(" .-0123456789") for q in output_text.split("\n") if q.strip()]
        questions = [q for q in questions if len(q) > 10]  # filter out short lines

        # Fallback if generation fails
        if not questions:
            questions = [
                "What is Machine Learning and its types?",
                "Tell me about one of your projects in detail.",
                "Explain a situation where you solved a technical problem.",
                "What tech stack did you use in your recent project?",
                "Explain what a neural network is."
            ]
        return random.sample(questions, min(num_questions, len(questions)))

    except Exception as e:
        print(f"⚠️ Error generating questions: {e}")
        return [
            "What is Machine Learning and its types?",
            "Explain the architecture of a Transformer model.",
            "What are your main technical skills?",
            "Describe your project experience in AI or ML.",
            "Explain how you handle model evaluation and improvement."
        ]
