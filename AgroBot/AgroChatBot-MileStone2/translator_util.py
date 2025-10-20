# from googletrans import Translator

# from deep_translator import GoogleTranslator
# from langdetect import detect

# translation = GoogleTranslator(source='auto', target='en').translate(text)


# translator = GoogleTranslator()

# def translate_text(text, dest="en"):
#     try:
#         result = translator.translate(text, dest=dest)
#         return result.text
#     except Exception as e:
#         print(f"Translation error: {e}")
#         return text

# def detect_language(text):
#     try:
#         result = translator.detect(text)
#         return result.lang
#     except Exception as e:
#         print(f"Language detection error: {e}")
#         return "en"




#translator_util.py
from langdetect import detect
from googletrans import Translator

translator = Translator()

def detect_language(text: str) -> str:
    """Detect language code (like en, hi, ta, te, ml, kn)."""
    try:
        lang = detect(text)
        return lang
    except Exception:
        return "en"

def translate_text(text: str, dest_lang: str) -> str:
    """Translate text safely."""
    try:
        if not text.strip():
            return ""
        return translator.translate(text, dest=dest_lang).text
    except Exception:
        return text
