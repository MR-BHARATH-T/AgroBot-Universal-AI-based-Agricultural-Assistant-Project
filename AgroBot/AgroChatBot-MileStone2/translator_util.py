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





from deep_translator import GoogleTranslator

translator = GoogleTranslator(source='auto', target='en')

def translate_text(text, dest="en"):
    try:
        result = GoogleTranslator(source='auto', target=dest).translate(text)
        return result
    except Exception as e:
        print(f"Translation error: {e}")
        return text

def detect_language(text):
    try:
        from langdetect import detect
        return detect(text)
    except Exception as e:
        print(f"Language detection error: {e}")
        return "en"
