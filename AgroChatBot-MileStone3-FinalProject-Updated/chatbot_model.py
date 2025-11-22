# chatbot_model.py
import os, json, re
from typing import Dict, Any
from langdetect import detect, DetectorFactory
import requests, traceback

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "openai/gpt-oss-20b:free")
APP_NAME = os.getenv("APP_NAME", "AgroBot Chat Assistant")
APP_URL = os.getenv("APP_URL", "http://127.0.0.1:5000")

DetectorFactory.seed = 0

try:
    from googletrans import Translator
    TRANSLATOR = Translator(); HAS_GOOGLETRANS = True
except Exception:
    TRANSLATOR = None; HAS_GOOGLETRANS = False
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY') or None
if OPENAI_API_KEY:
    try:
        import openai; openai.api_key = OPENAI_API_KEY; HAS_OPENAI = True
    except Exception:
        HAS_OPENAI = False
else:
    HAS_OPENAI = False
KB_PATH = os.path.join(os.path.dirname(__file__), 'kb.json')

def load_kb():
    if not os.path.exists(KB_PATH): return {}
    with open(KB_PATH,'r',encoding='utf-8') as f:
        data = json.load(f)
    out = {}
    if isinstance(data,list):
        for entry in data:
            keys = entry.get('keywords') or []
            if isinstance(keys,str): keys=[k.strip() for k in keys.split(',') if k.strip()]
            for k in keys:
                out[k.lower()] = {'en': entry.get('answer_en',''), 'hi': entry.get('answer_hi',''), 'ta': entry.get('answer_ta',''), 'ka': entry.get('answer_ka',''), 'ma': entry.get('answer_ma',''), 'te': entry.get('answer_te','')}
    elif isinstance(data,dict):
        for k,v in data.items():
            if isinstance(v,str): out[k.lower()] = {'en': v}
            elif isinstance(v,dict): out[k.lower()] = {'en': v.get('answer_en',''), 'hi': v.get('answer_hi',''), 'ta': v.get('answer_ta',''), 'ka': v.get('answer_ka',''), 'ma': v.get('answer_ma',''), 'te': v.get('answer_te','')}
    return out
KB = load_kb()

def detect_language(text: str) -> str:
    try: return detect(text)
    except Exception: return 'en'
    
def translate_text(text: str, dest: str) -> str:
    dest = dest[:2]
    if not HAS_GOOGLETRANS: return text
    try: return TRANSLATOR.translate(text, dest=dest).text
    except Exception: return text
    
def find_in_kb(message: str):
    m = message.lower()
    for k,v in KB.items():
        if k in m: return v
    tokens = re.findall(r"\w+", m)
    for k,v in KB.items():
        ktoks = re.findall(r"\w+", k)
        if any(t in ktoks for t in tokens if len(t)>3): return v
    return None

# def openai_fallback(user_profile: Dict[str,Any], message_text: str, target_lang: str='en') -> str:
#     if not HAS_OPENAI: return ''
#     try:
#         prompt = f"You are an expert agronomist. User profile: {user_profile}\nQuestion: {message_text}\nAnswer concisely."
#         resp = openai.ChatCompletion.create(model='gpt-4o-mini', messages=[{'role':'system','content':'You are an agronomist.'},{'role':'user','content':prompt}], max_tokens=300)
#         text = resp['choices'][0]['message']['content'].strip()
#         if target_lang and target_lang!='en' and HAS_GOOGLETRANS: text = translate_text(text, target_lang)
#         return text
#     except Exception:
#         return ''
    
def openrouter_fallback(user_profile: Dict[str, Any], message_text: str, target_lang: str = 'en') -> str:
    if not OPENROUTER_API_KEY:
        print("❌ OpenRouter: No API key configured.")
        return ""

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "X-Title": APP_NAME,
        "Referer": APP_URL
    }

    # Stronger instruction for model output
    system_prompt = (
        "You are an expert Indian agronomist. "
        "Always respond in clear, simple English unless explicitly asked for another language. "
        "Give short, practical, and region-specific farming advice."
    )

    # Clean, context-rich user message
    user_message = (
        f"User Profile: {json.dumps(user_profile, ensure_ascii=False)}\n\n"
        f"Question: {message_text}\n\n"
        f"Please answer in {target_lang.upper()} language only. "
        "Provide relevant soil, fertilizer, pest, and irrigation guidance in 4–6 concise lines."
    )

    payload = {
        "model": OPENROUTER_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        "max_tokens": 600,
        "temperature": 0.4
    }

    try:
        print(f"🌍 Sending request to OpenRouter model: {OPENROUTER_MODEL}")
        resp = requests.post(url, headers=headers, json=payload, timeout=30)

        if resp.status_code != 200:
            print(f"⚠️ OpenRouter error: {resp.status_code}")
            print("Response:", resp.text[:400])
            return ""

        data = resp.json()
        text = (
            data.get("choices", [{}])[0]
            .get("message", {})
            .get("content", "")
            .strip()
        )

        if not text:
            print("⚠️ Empty response text from OpenRouter:", data)
            return ""

        # Translate only if needed
        if target_lang != "en" and HAS_GOOGLETRANS:
            try:
                text = translate_text(text, target_lang)
            except Exception:
                pass

        print("✅ OpenRouter response received successfully.")
        return text

    except Exception as e:
        print("🔥 OpenRouter fallback failed:", str(e))
        traceback.print_exc()
        return ""
    
# def process_message(user_profile: Dict[str,Any], message_text: str) -> str:
#     if not message_text or not message_text.strip(): return 'Please ask a question about crops, soil, or pests.'
#     detected = detect_language(message_text)
#     if HAS_GOOGLETRANS and detected != 'en':
#         try: english_text = translate_text(message_text, 'en')
#         except Exception: english_text = message_text
#     else:
#         english_text = message_text
#     kb_item = find_in_kb(english_text)
#     if kb_item:
#         lang = (user_profile.get('preferred_language') or detected or 'en')[:2]
#         ans = kb_item.get(lang) or kb_item.get('en') or next(iter(kb_item.values()), '')
#         if not ans and kb_item.get('en') and lang!='en' and HAS_GOOGLETRANS:
#             ans = translate_text(kb_item.get('en'), lang)
#         return ans
#     if HAS_OPENAI:
#         resp = openai_fallback(user_profile or {}, english_text, target_lang=(user_profile.get('preferred_language') or detected or 'en')[:2])
#         if resp: return resp
#     # Try OpenRouter next
#     resp = openrouter_fallback(user_profile or {}, english_text, target_lang=(user_profile.get('preferred_language') or detected or 'en')[:2])
#     if resp:
#         return resp
#     return "I don't have that answer in KB. Try asking about a specific crop or pest."



def process_message(user_profile: Dict[str,Any], message_text: str) -> str:
    if not message_text or not message_text.strip():
        return 'Please ask a question about crops, soil, or pests.'

    detected = detect_language(message_text)
    target_lang = (user_profile.get('preferred_language') or detected or 'en')[:2]

    # translate incoming text to English for KB/search if needed
    english_text = message_text
    if HAS_GOOGLETRANS and detected != 'en':
        try:
            english_text = translate_text(message_text, 'en')
        except Exception:
            english_text = message_text

    # 1) KB lookup
    kb_item = find_in_kb(english_text)
    if kb_item:
        lang = target_lang
        ans = kb_item.get(lang) or kb_item.get('en') or next(iter(kb_item.values()), '')
        if not ans and kb_item.get('en') and lang != 'en' and HAS_GOOGLETRANS:
            try:
                ans = translate_text(kb_item.get('en'), lang)
            except Exception:
                ans = kb_item.get('en')
        return ans

    # 2) Try OpenAI fallback (if configured)
    if HAS_OPENAI:
        try:
            resp = openai_fallback(user_profile or {}, english_text, target_lang)
            if resp and resp.strip():
                return resp
        except Exception as e:
            print("OpenAI fallback error:", e)

    # 3) Try OpenRouter fallback
    try:
        resp = openrouter_fallback(user_profile or {}, english_text, target_lang)
        if resp and resp.strip():
            return resp
        else:
            print("OpenRouter fallback returned empty response.")
    except Exception as e:
        print("OpenRouter fallback error:", e)

    # 4) final friendly message if everything fails
    return ("⚠️ Sorry — I couldn't fetch an AI answer right now. "
            "Please check server logs, ensure OPENROUTER_API_KEY is valid, or try again shortly.")
