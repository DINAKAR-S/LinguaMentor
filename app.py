from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os
from db import init_db, log_mistake, get_all_mistakes
from prompt_templates import language_tutor_prompt
import uvicorn

app = FastAPI()
init_db()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "your-api-key")

class ChatRequest(BaseModel):
    known_language: str
    target_language: str
    level: str
    scene: str
    user_input: str
    turns: int = 0
    awaiting_conclusion: bool = False

AFFIRMATIVES = ["yes", "yeah", "ok", "okay", "ஆம்", "அம்மா", "sí", "oui"]
NEGATIVES = ["no", "nope", "இல்லை", "non", "illai", "na"]

@app.post("/chat")
def chat(req: ChatRequest):
    user_text = req.user_input.strip().lower()

    if req.awaiting_conclusion and any(x in user_text for x in AFFIRMATIVES):
        return get_review_summary_response()

    if req.awaiting_conclusion and any(x in user_text for x in NEGATIVES):
        return {"response": "👍 Great! Let's continue practicing. Type your next sentence."}

    if user_text in ["exit", "bye", "conclude"]:
        return get_review_summary_response()

    prompt = language_tutor_prompt.format(
        known_language=req.known_language,
        target_language=req.target_language,
        level=req.level,
        scene=req.scene,
        user_input=req.user_input
    )

    payload = {
        "model": "deepseek/deepseek-r1-zero:free",
        "messages": [
            {"role": "system", "content": "You are a helpful language tutor."},
            {"role": "user", "content": prompt}
        ]
    }

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        res = requests.post("https://openrouter.ai/api/v1/chat/completions", json=payload, headers=headers)
        res.raise_for_status()
        try:
            reply = res.json()["choices"][0]["message"]["content"]
            if not reply or "<tool_response>" in reply:
                reply = "⚠️ The AI had trouble responding. Please try saying that differently."
        except Exception as e:
            reply = f"⚠️ Error decoding AI response: {e}"


        if "✅" in reply and "🧠" in reply:
            log_mistake(req.user_input, "[Auto Correction]", reply)

        if req.turns > 0 and req.turns % 4 == 0:
            reply += "\n\n📝 Shall we conclude this session? (yes/no). You can also reply in your learning language."

        return {"response": reply}

    except Exception as e:
        return {"response": f"⚠️ Error: {str(e)}"}

@app.get("/review")
def review():
    return get_review_summary_response()

def get_review_summary_response():
    mistakes = get_all_mistakes()
    if not mistakes:
        return {
            "summary": [],
            "review_advice": "✅ You made no mistakes! Excellent work!",
            "response": "✅ Great session! Ready for another challenge?"
        }

    review_input = "\n".join(
        [f"User: {m[0]}\nCorrection: {m[1]}\nExplanation: {m[2]}" for m in mistakes]
    )

    prompt = f"""
You're a language tutor. Review the user's mistakes below:

{review_input}

Summarize:
1. Mistake types (Grammar, Vocabulary, etc.)
2. Common issues
3. 2–3 learning suggestions

End with: "Would you like to try a new scene or continue?"
"""

    payload = {
        "model": "deepseek/deepseek-r1-zero:free",
        "messages": [
            {"role": "system", "content": "You are a language coach."},
            {"role": "user", "content": prompt}
        ]
    }

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        res = requests.post("https://openrouter.ai/api/v1/chat/completions", json=payload, headers=headers)
        res.raise_for_status()
        feedback = res.json()["choices"][0]["message"]["content"]

        return {
            "summary": mistakes,
            "review_advice": feedback,
            "response": feedback
        }

    except Exception as e:
        return {
            "summary": [],
            "review_advice": f"⚠️ Could not generate review: {str(e)}",
            "response": f"⚠️ Could not generate review: {str(e)}"
        }


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=True)
