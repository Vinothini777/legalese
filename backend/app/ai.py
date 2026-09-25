import json
import urllib.request
import urllib.error
from .config import GEMINI_API_KEY, GEMINI_MODEL

SYSTEM_PROMPT = (
    "You are LegalEase, an educational legal-information assistant. "
    "Provide general legal information, not a substitute for a lawyer. "
    "Ask for jurisdiction when it materially affects the answer. "
    "Do not invent laws, cases, citations, sections or deadlines. "
    "Use this structure: Summary, Key Points, Possible Next Steps, Important Limitations."
)


def demo_response(issue, category):
    return f"""Summary\nYour question concerns {category.lower()}.\n\nKey Points\n- The exact legal position depends on the facts, documents and jurisdiction.\n- Keep copies of relevant agreements, notices, messages and other evidence.\n- Check the applicable government or court procedure for your location.\n\nPossible Next Steps\n- Write down the timeline of events.\n- Collect supporting documents.\n- Consider consulting a qualified lawyer or official legal-aid service.\n\nImportant Limitations\nThis is a demonstration response because no Gemini API key is configured.\nLegalEase provides educational information and is not a substitute for professional legal advice.\n\nQuestion received:\n{issue}"""


def generate_legal_response(issue, category):
    if not GEMINI_API_KEY:
        return demo_response(issue, category)
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"
    body = {"contents": [{"parts": [{"text": f"{SYSTEM_PROMPT}\nCategory: {category}\nUser question:\n{issue}"}]}]}
    request = urllib.request.Request(url, data=json.dumps(body).encode(), headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            data = json.loads(response.read().decode())
        text = data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text")
        return text.strip() if text else demo_response(issue, category)
    except Exception as exc:
        return demo_response(issue, category) + f"\n\nGemini connection note: {type(exc).__name__}"
