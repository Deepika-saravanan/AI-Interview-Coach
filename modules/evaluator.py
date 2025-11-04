from sentence_transformers import SentenceTransformer, util
from textblob import TextBlob

model = SentenceTransformer("all-MiniLM-L6-v2")

def evaluate_answer(question, answer_text):
    # Grammar correction
    corrected = str(TextBlob(answer_text).correct())
    grammar_score = 10 - (len(answer_text) - len(corrected)) / max(len(answer_text), 1) * 10
    grammar_score = max(0, round(grammar_score, 2))

    # Relevance check using semantic similarity
    q_emb = model.encode(question, convert_to_tensor=True)
    a_emb = model.encode(answer_text, convert_to_tensor=True)
    similarity = util.pytorch_cos_sim(q_emb, a_emb).item()
    relevance_score = round(similarity * 10, 2)

    # Combine
    final_score = round((grammar_score * 0.6) + (relevance_score * 0.4), 2)

    feedback = "Good answer, but you can explain more." if relevance_score > 5 else "Your answer seems off-topic. Try focusing on the question."

    return {
        "original": answer_text,
        "corrected": corrected,
        "grammar_score": grammar_score,
        "relevance_score": relevance_score,
        "final_score": final_score,
        "feedback": feedback
    }
