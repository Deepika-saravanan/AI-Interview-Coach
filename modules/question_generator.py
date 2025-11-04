# modules/question_generator.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

# a stronger instruction-tuned model
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}


def generate_questions_from_resume(resume_text: str, num_questions: int = 10):
    """
    Generate interview questions based on the given resume text
    using a Hugging Face instruction-tuned model.
    """
    prompt = (
        "You are an expert technical interviewer. "
        "Read the resume text below and generate "
        f"{num_questions} unique and professional interview questions "
        "that test the candidate’s knowledge in AI, Machine Learning, Python, and projects mentioned.\n\n"
        f"Resume:\n{resume_text}\n\n"
        "Return the questions as a numbered list like:\n"
        "1. ...\n2. ...\n"
    )

    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 400, "temperature": 0.7, "top_p": 0.9},
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        result = response.json()

        # extract generated text
        if isinstance(result, list) and len(result) > 0 and "generated_text" in result[0]:
            text = result[0]["generated_text"]
        else:
            text = str(result)

        # clean and split into questions
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        questions = [l for l in lines if any(word in l.lower() for word in ["what", "how", "why", "explain", "tell"])]

        # remove numbering artifacts and duplicates
        clean_q = []
        for q in questions:
            q = q.lstrip("0123456789. ").strip()
            if q not in clean_q:
                clean_q.append(q)

        # ensure we have at least a few questions
        return clean_q[:num_questions] if clean_q else ["Could not generate enough questions."]
    except Exception as e:
        print("Error generating questions:", e)
        # simple fallback
        return [
            "Describe one project mentioned in your resume.",
            "Explain the main technologies you used in your work.",
            "What challenges did you face in your recent project?",
            "How do you apply Machine Learning in real-world scenarios?",
            "What improvements would you make to your current skills?",
        ]
