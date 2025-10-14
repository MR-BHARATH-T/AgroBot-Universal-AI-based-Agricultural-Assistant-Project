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
#
# def detect_language(text):
#     try:
#         result = translator.detect(text)
#         return result.lang
#     except Exception as e:
#         print(f"Language detection error: {e}")
#         return "en"





# translator_util.py
from deep_translator import GoogleTranslator
from langdetect import detect

def detect_language(text):
    """Detect language of input text."""
    try:
        return detect(text)
    except Exception as e:
        print(f"[Translator] Language detection failed: {e}")
        return "en"

def translate_text(text, target_lang="en"):
    """Translate text to target language using deep-translator."""
    try:
        if not text.strip():
            return text

        source_lang = detect_language(text)
        if source_lang == target_lang:
            return text

        translated = GoogleTranslator(source=source_lang, target=target_lang).translate(text)
        return translated
    except Exception as e:
        print(f"[Translator] Translation error: {e}")
        return text
