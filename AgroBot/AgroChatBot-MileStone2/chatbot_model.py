# import os
# import random
# from dotenv import load_dotenv
# from openai import OpenAI

# from translator_util import translate_text, detect_language  # your translation module

# # ------------------- Load environment -------------------
# load_dotenv()
# api_key = os.getenv("OPENAI_API_KEY")
# client = None
# if api_key:
#     client = OpenAI(api_key=api_key)


# # ------------------- Greetings & Farewells -------------------
# greetings = {
#     "en": ["hello", "hi", "hey", "good morning", "good afternoon", "good evening"],
#     "ta": ["வணக்கம்", "ஹலோ"],
#     "hi": ["नमस्ते", "हैलो"],
#     "ml": ["ഹലോ", "നമസ്ക്കാരം"],
#     "te": ["హలో", "నమస్తే"]
# }

# greeting_responses = {
#     "en": ["Hello! How can I help you today?", "Hi there! Ask me anything about farming. 🌾"],
#     "ta": ["வணக்கம்! இன்று உங்களுக்கு எவ்வாறு உதவலாம்?"],
#     "hi": ["नमस्ते! खेती के बारे में मुझसे कुछ भी पूछें। 🌱"],
#     "ml": ["ഹലോ! കൃഷിയെ കുറിച്ച് എന്തെങ്കിലും ചോദിക്കാം. 🌿"],
#     "te": ["హలో! వ్యవసాయం గురించి ఏదైనా అడగండి. 🌱"]
# }

# farewells = {
#     "en": ["bye", "goodbye", "see you", "thanks", "thank you"],
#     "ta": ["பிரியாவிடை", "நன்றி"],
#     "hi": ["अलविदा", "धन्यवाद"],
#     "ml": ["വിട", "നന്ദി"],
#     "te": ["వీడ్కోలు", "ధన్యవాదాలు"]
# }

# farewell_responses = {
#     "en": ["Goodbye! Happy farming! 🌾", "You're welcome! 😊"],
#     "ta": ["வாழ்த்துகள்! மகிழ்ச்சியான விவசாயம்! 🌾"],
#     "hi": ["अलविदा! खेती में सफलता मिले! 🌱"],
#     "ml": ["വിട! സന്തോഷകരമായ കൃഷി ചെയ്യുക! 🌿"],
#     "te": ["వీడ్కోలు! సంతోషకరమైన వ్యవసాయం! 🌱"]
# }


# # ------------------- Offline Knowledge Base -------------------
# queries = {
#     "soil": {
#         # Cereals
#         "cotton": {
#             "en": "Cotton grows best in deep, fertile, well-drained sandy loam soil with good moisture retention.",
#             "ta": "பருத்தி ஆழமான, வளமான, நன்கு வடிகாலமைப்பு கொண்ட மணற்பாங்கு மண்ணில் சிறப்பாக வளரும்.",
#             "hi": "कपास गहरी, उपजाऊ, अच्छी जल निकासी वाली बलुई दोमट मिट्टी में अच्छी तरह उगती है।",
#             "ml": "പഞ്ചു ആഴമുള്ള, വളമുള്ള, നല്ല ഡ്രെയ്‌നേജ് ഉള്ള മണൽ-ചെങ്കല്ല് മണ്ണിൽ വളരുന്നു.",
#             "te": "పత్తి లోతైన, సారవంతమైన, బాగా డ్రైనేజీ ఉన్న ఇసుక లోమ్ మట్టిలో బాగా పెరుగుతుంది."
#         },
#         "rice": {
#             "en": "Rice grows best in clayey loam soil with good water retention.",
#             "ta": "அரிசி நல்ல நீர் தாங்கும் திறன் கொண்ட பஞ்சுப் பாங்கு மண்ணில் சிறப்பாக வளரும்.",
#             "hi": "चावल चिकनी दोमट मिट्टी में सबसे अच्छा उगता है जिसमें पानी की अच्छी धारण क्षमता होती है।",
#             "ml": "അരി നല്ല ജലധാരണമുള്ള മണ്ണിൽ മികച്ചതായി വളരുന്നു.",
#             "te": "బియ్యం మంచి నీరు నిల్వ చేసే మట్టిలో బాగా పెరుగుతుంది."
#         },
#         "wheat": {
#             "en": "Wheat prefers loamy or alluvial soil with good drainage.",
#             "ta": "கோதுமை நல்ல வடிகாலமைப்பு கொண்ட மணற்பாங்கு மண்ணில் வளரும்.",
#             "hi": "गेहूं अच्छे जल निकासी वाले दोमट या जलोढ़ मिट्टी में उगता है।",
#             "ml": "ഗോതമ്പ് നല്ല ഡ്രെയ്‌നേജ് ഉള്ള മണ്ണിൽ വളരുന്നു.",
#             "te": "గోధుమలు మంచి డ్రైనేజీ ఉన్న లోమ్ మట్టిలో బాగా పెరుగుతాయి."
#         },
#         "maize": {
#             "en": "Maize grows well in well-drained sandy loam or loamy soil rich in organic matter.",
#             "ta": "சோளம் நன்கு வடிகாலமைப்பு கொண்ட, உயிர்ச்சத்து நிறைந்த மணற்பாங்கு மண்ணில் வளரும்.",
#             "hi": "मक्का अच्छी जल निकासी वाली बलुई दोमट मिट्टी में अच्छी तरह उगता है।",
#             "ml": "ചോളം ജൈവവസ്തുക്കളിൽ സമ്പന്നമായ മണ്ണിൽ വളരുന്നു.",
#             "te": "మొక్కజొన్న సేంద్రీయ పదార్థాలతో సమృద్ధిగా ఉన్న మట్టిలో బాగా పెరుగుతుంది."
#         },

#         # Vegetables
#         "tomato": {
#             "en": "Tomatoes grow best in well-drained, fertile sandy loam soil with pH 6.0–6.8.",
#             "ta": "தக்காளி நன்கு வடிகாலமைப்பு கொண்ட வளமான மணற்பாங்கு மண்ணில் சிறப்பாக வளரும்.",
#             "hi": "टमाटर उपजाऊ बलुई दोमट मिट्टी में अच्छी तरह उगते हैं।",
#             "ml": "തക്കാളി വളമുള്ള മണൽ മണ്ണിൽ മികച്ചതായി വളരുന്നു.",
#             "te": "టమాటాలు మంచి డ్రైనేజీ ఉన్న మట్టిలో బాగా పెరుగుతాయి."
#         },
#         "potato": {
#             "en": "Potatoes prefer loose, well-drained loamy soil with good organic content.",
#             "ta": "உருளைக்கிழங்கு உயிர்ச்சத்து நிறைந்த மணற்பாங்கு மண்ணில் வளரும்.",
#             "hi": "आलू उपजाऊ दोमट मिट्टी में अच्छी तरह उगता है।",
#             "ml": "ഉരുളക്കിഴങ്ങ് നല്ല ജൈവവസ്തുക്കളുള്ള മണ്ണിൽ വളരുന്നു.",
#             "te": "బంగాళదుంపలు సేంద్రీయ పదార్థాలతో సమృద్ధిగా ఉన్న మట్టిలో బాగా పెరుగుతాయి."
#         },
#         "onion": {
#             "en": "Onions require well-drained sandy loam soil with neutral to slightly alkaline pH.",
#             "ta": "வெங்காயம் நன்கு வடிகாலமைப்பு கொண்ட மணற்பாங்கு மண்ணில் வளரும்.",
#             "hi": "प्याज बलुई दोमट मिट्टी में अच्छी तरह उगता है।",
#             "ml": "സവാള മണൽ മണ്ണിൽ മികച്ചതായി വളരുന്നു.",
#             "te": "ఉల్లిపాయలు లోమ్ మట్టిలో బాగా పెరుగుతాయి."
#         },
#         "carrot": {
#             "en": "Carrots grow well in deep, sandy, loose soil to allow root development.",
#             "ta": "காரட் ஆழமான மணற்பாங்கு மண்ணில் சிறப்பாக வளரும்.",
#             "hi": "गाजर रेतीली मिट्टी में अच्छी तरह उगता है।",
#             "ml": "കാരറ്റ് ആഴമുള്ള മണൽ മണ്ണിൽ വളരുന്നു.",
#             "te": "గాజర గడ్డి మట్టిలో బాగా పెరుగుతుంది."
#         },

#         # Fruits
#         "mango": {
#             "en": "Mangoes prefer deep, well-drained sandy loam soil rich in organic matter.",
#             "ta": "மாம்பழம் நன்கு வடிகாலமைப்பு கொண்ட வளமான மணற்பாங்கு மண்ணில் வளரும்.",
#             "hi": "आम बलुई दोमट मिट्टी में अच्छी तरह उगता है।",
#             "ml": "മാമ്പഴം വളമുള്ള മണ്ണിൽ വളരുന്നു.",
#             "te": "మామిడి లోమ్ మట్టిలో బాగా పెరుగుతుంది."
#         },
#         "banana": {
#             "en": "Bananas grow best in rich, well-drained loamy soil with high moisture retention.",
#             "ta": "வாழை உயர் ஈரப்பதம் கொண்ட மணற்பாங்கு மண்ணில் வளரும்.",
#             "hi": "केला उपजाऊ दोमट मिट्टी में अच्छी तरह उगता है।",
#             "ml": "വാഴപ്പഴം നല്ല ജലധാരണമുള്ള മണ്ണിൽ വളരുന്നു.",
#             "te": "అరటిపండ్లు లోమ్ మట్టిలో బాగా పెరుగుతాయి."
#         },
#         "apple": {
#             "en": "Apples require well-drained loamy soil with good fertility and slightly acidic pH.",
#             "ta": "ஆப்பிள் நல்ல வடிகாலமைப்பு கொண்ட மணற்பாங்கு மண்ணில் வளரும்.",
#             "hi": "सेब अम्लीय जल निकासी वाली मिट्टी में अच्छी तरह उगते हैं।",
#             "ml": "ആപ്പിൾ നല്ല മണ്ണിൽ വളരുന്നു.",
#             "te": "ఆపిల్ లోమ్ మట్టిలో బాగా పెరుగుతుంది."
#         },
#         "orange": {
#             "en": "Oranges grow best in deep, sandy loam soil with good drainage.",
#             "ta": "ஆரஞ்சு நன்கு வடிகாலமைப்பு கொண்ட மணற்பாங்கு மண்ணில் வளரும்.",
#             "hi": "संतरा बलुई मिट्टी में अच्छी तरह उगता है।",
#             "ml": "ഓറഞ്ച് നല്ല ഡ്രെയ്‌നേജ് ഉള്ള മണ്ണിൽ വളരുന്നു.",
#             "te": "నారింజలు ఇసుక మట్టిలో బాగా పెరుగుతాయి."
#         },
#         "grape": {
#             "en": "Grapes prefer well-drained sandy loam soil with moderate fertility.",
#             "ta": "திராட்சை மணற்பாங்கு மண்ணில் வளரும்.",
#             "hi": "अंगूर बलुई दोमट मिट्टी में अच्छी तरह उगते हैं।",
#             "ml": "മുന്തിരി നല്ല ഡ്രെയ്‌നേജ് ഉള്ള മണ്ണിൽ വളരുന്നു.",
#             "te": "ద్రాక్షలు ఇసుక మట్టిలో బాగా పెరుగుతాయి."
#         }
#     },

#     "fertilizer": {
#         "en": [
#             "Use organic compost and nitrogen-rich fertilizer for better yield.",
#             "Phosphorus and potassium fertilizers help root growth.",
#             "Apply balanced NPK fertilizer according to soil test results."
#         ],
#         "ta": ["மேல்தரம் விளைச்சல் பெற உயிர்ச்சத்து நிறைந்த உரம் பயன்படுத்தவும்.", "வேர் வளர்ச்சிக்கு பாஸ்பரஸ் மற்றும் பொட்டாசியம் உரங்கள் உதவும்."],
#         "hi": ["बेहतर उपज के लिए कार्बनिक खाद और नाइट्रोजन-समृद्ध उर्वरक का उपयोग करें।", "जड़ विकास के लिए फॉस्फोरस और पोटेशियम उर्वरक मदद करते हैं।"],
#         "ml": ["മികച്ച വിളവിന് ജൈവ വളവും നൈട്രജൻ സമ്പന്ന വളവും ഉപയോഗിക്കുക."],
#         "te": ["మంచి దిగుబడికి ఆర్గానిక్ కాంపోస్ట్ మరియు నిట్రోజన్-రిచ్ ఎరువులను ఉపయోగించండి."]
#     },

#     "pest": {
#         "en": [
#             "Neem oil is effective against many pests.",
#             "Use natural pesticides like garlic or chili extracts for eco-friendly farming.",
#             "Regular monitoring and crop rotation help reduce pest attacks."
#         ],
#         "ta": ["நீம் எண்ணெய் பல பூச்சிகளுக்கு விளைவுள்ளது."],
#         "hi": ["नीम का तेल कई कीड़ों के खिलाफ प्रभावी है।"],
#         "ml": ["നീം എണ്ണ പല കീടങ്ങൾക്ക് ഫലപ്രദമാണ്."],
#         "te": ["నీమోయిల్ చాలా pests కు సమర్థవంతంగా పనిచేస్తుంది."]
#     },

#     "harvest": {
#         "en": "Harvesting depends on the crop type. Ensure proper maturity before harvesting for best yield.",
#         "ta": "பழங்கள் அறுவடை செய்யும் முன் சரியான வளர்ச்சி பெற்றிருப்பதை உறுதி செய்யுங்கள்.",
#         "hi": "फसल की कटाई प्रकार पर निर्भर करती है। सर्वोत्तम उपज के लिए सही परिपक्वता सुनिश्चित करें।",
#         "ml": "വളവു വിളവെടുപ്പ് വിളയുടെ തരത്തിൽ ആശ്രിതമാണ്. നല്ല വിളവിന് പൂർണമായ വളർച്ച ഉറപ്പാക്കുക.",
#         "te": "ఫలితానికి సరైన పాకవయసు వచ్చి ఉన్నట్లు నిర్ధారించండి."
#     }
# }


# # ------------------- Functions -------------------

# def get_offline_response(user_input: str, lang="en"):
#     user_input_lower = user_input.lower()
#     # Greetings & Farewells handled in process_message
#     # Soil
#     for crop, translations in queries.get("soil", {}).items():
#         if crop in user_input_lower:
#             return translations.get(lang, translations.get("en"))
#     # Other topics
#     for topic in ["fertilizer", "pest", "harvest"]:
#         if topic in user_input_lower:
#             resp = queries.get(topic, {}).get(lang, queries.get(topic, {}).get("en"))
#             return random.choice(resp) if isinstance(resp, list) else resp
#     return None


# def ask_openai(user_input: str):
#     if not client:
#         return None
#     try:
#         response = client.chat.completions.create(
#             # model="gpt-4o-mini",
#             base_url="https://openrouter.ai/api/v1",
#             model="deepseek / deepseek - chat - v3.1: free",
#             messages=[
#                 {"role": "system", "content": "You are an agriculture assistant. Reply clearly and concisely."},
#                 {"role": "user", "content": user_input}
#             ],
#             temperature=0.5
#         )
#         return response.choices[0].message.content.strip()
#     except Exception as e:
#         print(f"OpenAI error: {e}")
#         return None


# def process_message(user_input, dest_lang=None):
#     """
#     1. Detect user language
#     2. Check for greetings/farewells
#     3. Offline knowledge base first
#     4. OpenAI fallback
#     5. Offline default fallback
#     """
#     try:
#         user_lang = detect_language(user_input)
#     except:
#         user_lang = "en"

#     if not dest_lang:
#         dest_lang = user_lang

#     # --- Step 0: Greetings ---
#     user_input_lower = user_input.lower()
#     for lang, greet_list in greetings.items():
#         if any(greet.lower() in user_input_lower for greet in greet_list):
#             return random.choice(greeting_responses.get(lang, greeting_responses["en"]))

#     # --- Step 0b: Farewells ---
#     for lang, bye_list in farewells.items():
#         if any(word.lower() in user_input_lower for word in bye_list):
#             return random.choice(farewell_responses.get(lang, farewell_responses["en"]))

#     # --- Step 1: Offline KB ---
#     response = get_offline_response(user_input, lang=dest_lang)
#     if response:
#         return response

#     # --- Step 2: OpenAI fallback ---
#     response = ask_openai(user_input)
#     if response:
#         if dest_lang != "en":
#             try:
#                 response = translate_text(response, dest=dest_lang)
#             except:
#                 pass
#         return response

#     # --- Step 3: Offline default fallback ---
#     defaults = {
#         "en": "I couldn’t find an answer. Please ask about soil, fertilizer, pests, or harvesting.",
#         "ta": "நான் பதிலை கண்டறிய முடியவில்லை. தயவுசெய்து மணல், உரம், பூச்சிகள் அல்லது அறுவடை பற்றி கேளுங்கள்.",
#         "hi": "मैं उत्तर नहीं पा सका। कृपया मिट्टी, उर्वरक, कीट या कटाई के बारे में पूछें।",
#         "ml": "ഞാൻ ഒരു ഉത്തരം കണ്ടെത്താനായില്ല. ദയവായി മണ്ണ്, വളം, കീടങ്ങൾ അല്ലെങ്കിൽ വിളവെടുപ്പ് ചോദിക്കുക.",
#         "te": "నేను సమాధానం కనుగొనలేకపోయాను. దయచేసి మట్టీ, ఎరువు, కీటకాల లేదా ఫలితాల గురించి అడగండి."
#     }
#     return defaults.get(dest_lang, defaults["en"])








# import os
# import random
# from dotenv import load_dotenv
# import openai

# from translator_util import translate_text, detect_language  # your translation module

# # ------------------- Load environment -------------------
# load_dotenv()
# api_key = os.getenv("OPENAI_API_KEY")
# openrouter_key = os.getenv("OPENROUTER_API_KEY")  # Optional if using OpenRouter

# if api_key:
#     openai.api_key = api_key

# # If using OpenRouter, override API base URL
# OPENROUTER_BASE = "https://openrouter.ai/api/v1"

# # ------------------- Greetings & Farewells -------------------
# greetings = {
#     "en": ["hello", "hi", "hey", "good morning", "good afternoon", "good evening"],
#     "ta": ["வணக்கம்", "ஹலோ"],
#     "hi": ["नमस्ते", "हैलो"],
#     "ml": ["ഹലോ", "നമസ്ക്കാരം"],
#     "te": ["హలో", "నమస్తే"],
#     "kn": ["ಹಲೋ", "ನಮಸ್ಕಾರ"]
# }

# greeting_responses = {
#     "en": ["Hello! How can I help you today?", "Hi there! Ask me anything about farming. 🌾"],
#     "ta": ["வணக்கம்! இன்று உங்களுக்கு எவ்வாறு உதவலாம்?"],
#     "hi": ["नमस्ते! खेती के बारे में मुझसे कुछ भी पूछें। 🌱"],
#     "ml": ["ഹലോ! കൃഷിയെ കുറിച്ച് എന്തെങ്കിലും ചോദിക്കാം. 🌿"],
#     "te": ["హలో! వ్యవసాయం గురించి ఏదైనా అడగండి. 🌱"],
#     "kn": ["ಹಲೋ! ಕೃಷಿ ಬಗ್ಗೆ ಏನಾದರೂ ಕೇಳಿ. 🌾"]
# }

# farewells = {
#     "en": ["bye", "goodbye", "see you", "thanks", "thank you"],
#     "ta": ["பிரியாவிடை", "நன்றி"],
#     "hi": ["अलविदा", "धन्यवाद"],
#     "ml": ["വിട", "നന്ദി"],
#     "te": ["వీడ్కోలు", "ధన్యవాదాలు"],
#     "kn": ["ವಿದಾಯ", "ಧನ್ಯವಾದಗಳು"]
# }

# farewell_responses = {
#     "en": ["Goodbye! Happy farming! 🌾", "You're welcome! 😊"],
#     "ta": ["வாழ்த்துகள்! மகிழ்ச்சியான விவசாயம்! 🌾"],
#     "hi": ["अलविदा! खेती में सफलता मिले! 🌱"],
#     "ml": ["വിട! സന്തോഷകരമായ കൃഷി ചെയ്യുക! 🌿"],
#     "te": ["వీడ్కోలు! సంతోషకరమైన వ్యవసాయం! 🌱"],
#     "kn": ["ವಿದಾಯ! ಸಂತೋಷಕರ ಕೃಷಿ! 🌾", "ಸ್ವಾಗತ! 😊"]
# }

# # ------------------- Offline Knowledge Base -------------------
# # Keep your existing `queries` dictionary as-is

# queries = {
#     "soil": {
#         # Cereals
#         "cotton": {
#             "en": "Cotton grows best in deep, fertile, well-drained sandy loam soil with good moisture retention.",
#             "ta": "பருத்தி ஆழமான, வளமான, நன்கு வடிகாலமைப்பு கொண்ட மணற்பாங்கு மண்ணில் சிறப்பாக வளரும்.",
#             "hi": "कपास गहरी, उपजाऊ, अच्छी जल निकासी वाली बलुई दोमट मिट्टी में अच्छी तरह उगती है।",
#             "ml": "പഞ്ചു ആഴമുള്ള, വളമുള്ള, നല്ല ഡ്രെയ്‌നേജ് ഉള്ള മണൽ-ചെങ്കല്ല് മണ്ണിൽ വളരുന്നു.",
#             "te": "పత్తి లోతైన, సారవంతమైన, బాగా డ్రైనేజీ ఉన్న ఇసుక లోమ్ మట్టిలో బాగా పెరుగుతుంది.",
#             "kn": "ಹತ್ತಿ ಹಣ್ಣು ಉಗಲು ಉತ್ತಮವಾಗಿ, ಹಣ್ಣಿನತ್ತಿರುವ, ಫಲವತ್ತಾದ, ಚೆನ್ನಾಗಿ ನಿಗದಿತ ಉಪ್ಪಿನ ಮಣ್ಣಿನಲ್ಲಿ ಬೆಳೆಯುತ್ತದೆ."
#         },
#         "rice": {
#             "en": "Rice grows best in clayey loam soil with good water retention.",
#             "ta": "அரிசி நல்ல நீர் தாங்கும் திறன் கொண்ட பஞ்சுப் பாங்கு மண்ணில் சிறப்பாக வளரும்.",
#             "hi": "चावल चिकनी दोमट मिट्टी में सबसे अच्छा उगता है जिसमें पानी की अच्छी धारण क्षमता होती है।",
#             "ml": "അരി നല്ല ജലധാരണമുള്ള മണ്ണിൽ മികച്ചതായി വളരുന്നു.",
#             "te": "బియ్యం మంచి నీరు నిల్వ చేసే మట్టిలో బాగా పెరుగుతుంది.",
#             "kn": "ಅಕ್ಕಿ ಉತ್ತಮವಾಗಿ ಬೆಳೆದಿರಲು, ಮಣ್ಣಿನಲ್ಲಿನ ನೀರಿನ ಉತ್ತಮ ನಿರೋಧಕತೆಯೊಂದಿಗೆ ಮಣ್ಣಿನಲ್ಲಿಯೇ ಬೆಳೆಯುತ್ತದೆ."
#         },
#         "wheat": {
#             "en": "Wheat prefers loamy or alluvial soil with good drainage.",
#             "ta": "கோதுமை நல்ல வடிகாலமைப்பு கொண்ட மணற்பாங்கு மண்ணில் வளரும்.",
#             "hi": "गेहूं अच्छे जल निकासी वाले दोमट या जलोढ़ मिट्टी में उगता है।",
#             "ml": "ഗോതമ്പ് നല്ല ഡ്രെയ്‌നേജ് ഉള്ള മണ്ണിൽ വളരുന്നു.",
#             "te": "గోధుమలు మంచి డ్రైనేజీ ఉన్న లోమ్ మట్టిలో బాగా పెరుగుతాయి.",
#             "kn": "ಗೋಧು ಉತ್ತಮವಾಗಿ ಬೆಳೆಯಲು, ನಿಗದಿತ ಅಥವಾ ನದಿ ತೀರದ ಮಣ್ಣಿನಲ್ಲಿ ಬೆಳೆದು ಬೆಳೆಯುತ್ತದೆ."
#         },
#         "maize": {
#             "en": "Maize grows well in well-drained sandy loam or loamy soil rich in organic matter.",
#             "ta": "சோளம் நன்கு வடிகாலமைப்பு கொண்ட, உயிர்ச்சத்து நிறைந்த மணற்பாங்கு மண்ணில் வளரும்.",
#             "hi": "मक्का अच्छी जल निकासी वाली बलुई दोमट मिट्टी में अच्छी तरह उगता है।",
#             "ml": "ചോളം ജൈവവസ്തുക്കളിൽ സമ്പന്നമായ മണ്ണിൽ വളരുന്നു.",
#             "te": "మొక్కజొన్న సేంద్రీయ పదార్థాలతో సమృద్ధిగా ఉన్న మట్టిలో బాగా పెరుగుతుంది.",
#             "kn": "ಮಕ್ಕಾ ಉತ್ತಮವಾಗಿ ಬೆಳೆಯಲು, ನಂದವಾದ, ಜೈವಿಕ ವಸ್ತುಗಳಿಂದ ಸಮೃದ್ಧ ಮಣ್ಣಿನಲ್ಲಿ ಬೆಳೆದು ಬೆಳೆಯುತ್ತದೆ."
#         },

#         # Vegetables
#         "tomato": {
#             "en": "Tomatoes grow best in well-drained, fertile sandy loam soil with pH 6.0–6.8.",
#             "ta": "தக்காளி நன்கு வடிகாலமைப்பு கொண்ட வளமான மணற்பாங்கு மண்ணில் சிறப்பாக வளரும்.",
#             "hi": "टमाटर उपजाऊ बलुई दोमट मिट्टी में अच्छी तरह उगते हैं।",
#             "ml": "തക്കാളി വളമുള്ള മണൽ മണ്ണിൽ മികച്ചതായി വളരുന്നു.",
#             "te": "టమాటాలు మంచి డ్రైనేజీ ఉన్న మట్టిలో బాగా పెరుగుతాయి.",
#             "kn": "ಟೊಮೇಟೋ ಉತ್ತಮವಾಗಿ ಬೆಳೆಯಲು, ಚೆನ್ನಾಗಿ ನಿಗದಿತ, ಫಲವತ್ತಾದ ಉಪ್ಪಿನ ಮಣ್ಣಿನಲ್ಲಿ (pH 6.0–6.8) ಬೆಳೆದು ಬೆಳೆಯುತ್ತದೆ."
#         },
#         "potato": {
#             "en": "Potatoes prefer loose, well-drained loamy soil with good organic content.",
#             "ta": "உருளைக்கிழங்கு உயிர்ச்சத்து நிறைந்த மணற்பாங்கு மண்ணில் வளரும்.",
#             "hi": "आलू उपजाऊ दोमट मिट्टी में अच्छी तरह उगता है।",
#             "ml": "ഉരുളക്കിഴങ്ങ് നല്ല ജൈവവസ്തുക്കളുള്ള മണ്ണിൽ വളരുന്നു.",
#             "te": "బంగాళదుంపలు సేంద్రీయ పదార్థాలతో సమృద్ధిగా ఉన్న మట్టిలో బాగా పెరుగుతాయి.",
#             "kn": "ಆಲೂಗಡ್ಡೆ ಉತ್ತಮವಾಗಿ ಬೆಳೆಯಲು, ನಿಗದಿತ, ಚೆನ್ನಾಗಿ ನಿಗದಿತ, ಜೈವಿಕ ವಸ್ತುಗಳಿಂದ ಸಮೃದ್ಧ ಮಣ್ಣಿನಲ್ಲಿ ಬೆಳೆದು ಬೆಳೆಯುತ್ತದೆ."
#         },
#         "onion": {
#             "en": "Onions require well-drained sandy loam soil with neutral to slightly alkaline pH.",
#             "ta": "வெங்காயம் நன்கு வடிகாலமைப்பு கொண்ட மணற்பாங்கு மண்ணில் வளரும்.",
#             "hi": "प्याज बलुई दोमट मिट्टी में अच्छी तरह उगता है।",
#             "ml": "സവാള മണൽ മണ്ണിൽ മികച്ചതായി വളരുന്നു.",
#             "te": "ఉల్లిపాయలు లోమ్ మట్టిలో బాగా పెరుగుతాయి.",
#             "kn": "ಈರುಳ್ಳಿ ಉತ್ತಮವಾಗಿ ಬೆಳೆಯಲು, ಚೆನ್ನಾಗಿ ನಿಗದಿತ ಉಪ್ಪಿನ ಮಣ್ಣಿನಲ್ಲಿ, ಸ್ತಿತಿಯಿಂದ ಸ್ವಲ್ಪ ಆಲ್ಕಲೈನ್ pH ಅಗತ್ಯವಿದೆ."
#         },
#         "carrot": {
#             "en": "Carrots grow well in deep, sandy, loose soil to allow root development.",
#             "ta": "காரட் ஆழமான மணற்பாங்கு மண்ணில் சிறப்பாக வளரும்.",
#             "hi": "गाजर रेतीली मिट्टी में अच्छी तरह उगता है।",
#             "ml": "കാരറ്റ് ആഴമുള്ള മണൽ മണ്ണിൽ വളരുന്നു.",
#             "te": "గాజర గడ్డి మట్టిలో బాగా పెరుగుతుంది.",
#             "kn": "ಗಾರ್ಲೆಟ್ ಉತ್ತಮವಾಗಿ ಬೆಳೆಯಲು, ಆಳವಾದ, ನಂದವಾದ, ಬಿಸಿಲು ಮಣ್ಣು, ಬೆಳ್ಳುಳ್ಳಿ ಬೆಳವಣಿಗೆಯನ್ನು ಅನುಮತಿಸುತ್ತದೆ."
#         },

#         # Fruits
#         "mango": {
#             "en": "Mangoes prefer deep, well-drained sandy loam soil rich in organic matter.",
#             "ta": "மாம்பழம் நன்கு வடிகாலமைப்பு கொண்ட வளமான மணற்பாங்கு மண்ணில் வளரும்.",
#             "hi": "आम बलुई दोमट मिट्टी में अच्छी तरह उगता है।",
#             "ml": "മാമ്പഴം വളമുള്ള മണ്ണിൽ വളരുന്നു.",
#             "te": "మామిడి లోమ్ మట్టిలో బాగా పెరుగుతుంది.",
#             "kn": "ಮಾವಿನ ಮರ ಉತ್ತಮವಾಗಿ ಬೆಳೆಯಲು, ಆಳವಾದ, ಚೆನ್ನಾಗಿ ನಿಗದಿತ, ಜೈವಿಕ ವಸ್ತುಗಳಿಂದ ಸಮೃದ್ಧ ಮಣ್ಣಿನಲ್ಲಿ ಬೆಳೆಯುತ್ತದೆ."
#         },
#         "banana": {
#             "en": "Bananas grow best in rich, well-drained loamy soil with high moisture retention.",
#             "ta": "வாழை உயர் ஈரப்பதம் கொண்ட மணற்பாங்கு மண்ணில் வளரும்.",
#             "hi": "केला उपजाऊ दोमट मिट्टी में अच्छी तरह उगता है।",
#             "ml": "വാഴപ്പഴം നല്ല ജലധാരണമുള്ള മണ്ണിൽ വളരുന്നു.",
#             "te": "అరటిపండ్లు లోమ్ మట్టిలో బాగా పెరుగుతాయి.",
#             "kn": "ಬಾಳೆಹಣ್ಣು ಉತ್ತಮವಾಗಿ ಬೆಳೆಯಲು, ಸಮೃದ್ಧ, ಚೆನ್ನಾಗಿ ನಿಗದಿತ ಉಪ್ಪಿನ ಮಣ್ಣು, ಹೆಚ್ಚಿನ ನೀರಿನ ನಿರೋಧಕತೆಯೊಂದಿಗೆ ಬೆಳೆದು ಬೆಳೆಯುತ್ತದೆ."
#         },
#         "apple": {
#             "en": "Apples require well-drained loamy soil with good fertility and slightly acidic pH.",
#             "ta": "ஆப்பிள் நல்ல வடிகாலமைப்பு கொண்ட மணற்பாங்கு மண்ணில் வளரும்.",
#             "hi": "सेब अम्लीय जल निकासी वाली मिट्टी में अच्छी तरह उगते हैं।",
#             "ml": "ആപ്പിൾ നല്ല മണ്ണിൽ വളരുന്നു.",
#             "te": "ఆపిల్ లోమ్ మట్టిలో బాగా పెరుగుతుంది.",
#             "kn": "ಸೇಬು ಉತ್ತಮವಾಗಿ ಬೆಳೆಯಲು, ಚೆನ್ನಾಗಿ ನಿಗದಿತ ಉಪ್ಪಿನ ಮಣ್ಣು, ಉತ್ತಮ ಫಲವತ್ತತೆ ಮತ್ತು ಸ್ವಲ್ಪ ಆಮ್ಲ pH ಅಗತ್ಯವಿದೆ."
#         },
#         "orange": {
#             "en": "Oranges grow best in deep, sandy loam soil with good drainage.",
#             "ta": "ஆரஞ்சு நன்கு வடிகாலமைப்பு கொண்ட மணற்பாங்கு மண்ணில் வளரும்.",
#             "hi": "संतरा गहरी बलुई दोमट मिट्टी में अच्छी तरह उगता है।",
#             "ml": "ഓറഞ്ച് ആഴമുള്ള മണൽ മണ്ണിൽ വളരുന്നു.",
#             "te": "కిర్రిగువ橙 లోమ్ మట్టిలో బాగా పెరుగుతుంది.",
#             "kn": "ಕಿತ್ತಳೆ ಉತ್ತಮವಾಗಿ ಬೆಳೆಯಲು, ಆಳವಾದ, ಚೆನ್ನಾಗಿ ನಿಗದಿತ ಉಪ್ಪಿನ ಮಣ್ಣಿನಲ್ಲಿ ಬೆಳೆದು ಬೆಳೆಯುತ್ತದೆ."
#         },
#         "grape": {
#             "en": "Grapes prefer well-drained, fertile sandy loam soil with moderate pH.",
#             "ta": "திராட்சை வளமான மணற்பாங்கு மண்ணில் வளரும்.",
#             "hi": "अंगूर उपजाऊ दोमट मिट्टी में अच्छी तरह उगते हैं।",
#             "ml": "അങ്ങൂരം വളമുള്ള മണൽ മണ്ണിൽ വളരുന്നു.",
#             "te": "ద్రాక్ష లోమ్ మట్టిలో బాగా పెరుగుతుంది.",
#             "kn": "ದ್ರಾಕ್ಷೆ ಉತ್ತಮವಾಗಿ ಬೆಳೆಯಲು, ಚೆನ್ನಾಗಿ ನಿಗದಿತ, ಫಲವತ್ತಾದ ಉಪ್ಪಿನ ಮಣ್ಣಿನಲ್ಲಿ ಬೆಳೆದು ಬೆಳೆಯುತ್ತದೆ."
#         }
#     },

#     "fertilizer": {
#         "en": [
#             "Use organic compost and nitrogen-rich fertilizer for better yield.",
#             "Phosphorus and potassium fertilizers help root growth.",
#             "Apply balanced NPK fertilizer according to soil test results."
#         ],
#         "ta": ["மேல்தரம் விளைச்சல் பெற உயிர்ச்சத்து நிறைந்த உரம் பயன்படுத்தவும்.", "வேர் வளர்ச்சிக்கு பாஸ்பரஸ் மற்றும் பொட்டாசியம் உரங்கள் உதவும்."],
#         "hi": ["बेहतर उपज के लिए कार्बनिक खाद और नाइट्रोजन-समृद्ध उर्वरक का उपयोग करें।", "जड़ विकास के लिए फॉस्फोरस और पोटेशियम उर्वरक मदद करते हैं।"],
#         "ml": ["മികച്ച വിളവിന് ജൈവ വളവും നൈട്രജൻ സമ്പന്ന വളവും ഉപയോഗിക്കുക."],
#         "te": ["మంచి దిగుబడికి ఆర్గానిక్ కాంపోస్ట్ మరియు నిట్రోజన్-రిచ్ ఎరువులను ఉపయోగించండి."],
#         "kn": ["ಉತ್ತಮ ಫಲಿತಾಂಶಕ್ಕಾಗಿ, ಜೈವಿಕ ರಸ ಮತ್ತು ನೈಟ್ರೋಜನ್-ಸಂಪನ್ನ ಎರೆವುಗಳನ್ನು ಬಳಸಿರಿ.", "ಮೂಲಿಕ ವೃದ್ಧಿಗೆ ಫಾಸ್ಫೋರಸ್ ಮತ್ತು ಪೊಟ್ಯಾಸಿಯಂ ಎರೆವುಗಳು ಸಹಾಯ ಮಾಡುತ್ತವೆ."]
#     },

#     "pest": {
#         "en": [
#             "Neem oil is effective against many pests.",
#             "Use natural pesticides like garlic or chili extracts for eco-friendly farming.",
#             "Regular monitoring and crop rotation help reduce pest attacks."
#         ],
#         "ta": ["நீம் எண்ணெய் பல பூச்சிகளுக்கு விளைவுள்ளது."],
#         "hi": ["नीम का तेल कई कीड़ों के खिलाफ प्रभावी है।"],
#         "ml": ["നീം എണ്ണ പല കീടങ്ങൾക്ക് ഫലപ്രദമാണ്."],
#         "te": ["నీమోయిల్ చాలా pests కు సమర్థవంతంగా పనిచేస్తుంది."],
#         "kn": ["ನೀಮ್ ಎಣ್ಣೆ ಹಲವಾರು ಕೀಟಗಳ ವಿರುದ್ಧ ಪರಿಣಾಮಕಾರಿಯಾಗಿದೆ.", "ಹೆಸರು ಅಥವಾ ಮೆಣಸಿನ ಕಾಳುಗಳಂತಹ ನೈಸರ್ಗಿಕ ಕೀಟನಾಶಕಗಳನ್ನು ಪರಿಸರ ಸ್ನೇಹಿ ಕೃಷಿಗಾಗಿ ಬಳಸಿರಿ.", "ನಿಯಮಿತವಾಗಿ ಮೇಲ್ವಿಚಾರಣೆ ಮತ್ತು ಬೆಳೆ ಬದಲಾವಣೆ ಕೀಟದ ದಾಳಿಗಳನ್ನು ಕಡಿಮೆ ಮಾಡಲು ಸಹಾಯ ಮಾಡುತ್ತದೆ."]
#     },

#     "harvest": {
#         "en": "Harvesting depends on the crop type. Ensure proper maturity before harvesting for best yield.",
#         "ta": "பழங்கள் அறுவடை செய்யும் முன் சரியான வளர்ச்சி பெற்றிருப்பதை உறுதி செய்யுங்கள்.",
#         "hi": "फसल की कटाई प्रकार पर निर्भर करती है। सर्वोत्तम उपज के लिए सही परिपक्वता सुनिश्चित करें।",
#         "ml": "വളവു വിളവെടുപ്പ് വിളയുടെ തരത്തിൽ ആശ്രിതമാണ്. നല്ല വിളവിന് പൂർണമായ വളർച്ച ഉറപ്പാക്കുക.",
#         "te": "ఫలితానికి సరైన పాకవయసు వచ్చి ఉన్నట్లు నిర్ధారించండి.",
#         "kn": "ಹೆಸರು ಬಗೆಯ ಮೇಲೆ ಅವಲಂಬಿತವಾಗಿರುವುದು. ಉತ್ತಮ ಫಲಿತಾಂಶಕ್ಕಾಗಿ, ಕಟಾಯಿಸುವ ಮೊದಲು ಸರಿಯಾದ ಪಾಕವಯಸ್ಸು ಖಚಿತಪಡಿಸಿಕೊಳ್ಳಿ."
#     }
# }


# # ------------------- Functions -------------------

# def get_offline_response(user_input: str, lang="en"):
#     user_input_lower = user_input.lower()
#     for crop, translations in queries.get("soil", {}).items():
#         if crop in user_input_lower:
#             return translations.get(lang, translations.get("en"))
#     for topic in ["fertilizer", "pest", "harvest"]:
#         if topic in user_input_lower:
#             resp = queries.get(topic, {}).get(lang, queries.get(topic, {}).get("en"))
#             return random.choice(resp) if isinstance(resp, list) else resp
#     return None

# # ------------------- OpenAI / OpenRouter -------------------

# def ask_openai(user_input: str):
#     try:
#         # Use OpenRouter via OpenAI SDK
#         response = openai.ChatCompletion.create(
#             model="deepseek/deepseek-chat-v3.1:free",  # your OpenRouter model
#             messages=[
#                 {"role": "system", "content": "You are an agriculture assistant. Reply clearly and concisely."},
#                 {"role": "user", "content": user_input}
#             ],
#             temperature=0.5,
#             api_key=api_key,
#             base=OPENROUTER_BASE if openrouter_key else None
#         )
#         return response.choices[0].message.content.strip()
#     except Exception as e:
#         print(f"OpenAI/OpenRouter error: {e}")
#         return None

# # ------------------- Main Processing -------------------

# def process_message(user_input, dest_lang=None):
#     try:
#         user_lang = detect_language(user_input)
#     except:
#         user_lang = "en"

#     if not dest_lang:
#         dest_lang = user_lang

#     user_input_lower = user_input.lower()

#     # Greetings
#     for lang, greet_list in greetings.items():
#         if any(greet.lower() in user_input_lower for greet in greet_list):
#             return random.choice(greeting_responses.get(lang, greeting_responses["en"]))

#     # Farewells
#     for lang, bye_list in farewells.items():
#         if any(word.lower() in user_input_lower for word in bye_list):
#             return random.choice(farewell_responses.get(lang, farewell_responses["en"]))

#     # Offline KB
#     response = get_offline_response(user_input, lang=dest_lang)
#     if response:
#         return response

#     # OpenAI / OpenRouter fallback
#     response = ask_openai(user_input)
#     if response:
#         if dest_lang != "en":
#             try:
#                 response = translate_text(response, dest=dest_lang)
#             except:
#                 pass
#         return response

#     # Offline default fallback
#     defaults = {
#         "en": "I couldn’t find an answer. Please ask about soil, fertilizer, pests, or harvesting.",
#         "ta": "நான் பதிலை கண்டறிய முடியவில்லை. தயவுசெய்து மணல், உரம், பூச்சிகள் அல்லது அறுவடை பற்றி கேளுங்கள்.",
#         "hi": "मैं उत्तर नहीं पा सका। कृपया मिट्टी, उर्वरक, कीट या कटाई के बारे में पूछें।",
#         "ml": "ഞാൻ ഒരു ഉത്തരം കണ്ടെത്താനായില്ല. ദയവായി മണ്ണ്, വളം, കീടങ്ങൾ അല്ലെങ്കിൽ വിളവെടുപ്പ് ചോദിക്കുക.",
#         "te": "నేను సమాధానం కనుగొనలేకపోయాను. దయచేసి మట్టీ, ఎరువు, కీటకాల లేదా ఫలితాల గురించి అడగండి.",
#         "kn": "ನಾನು ಉತ್ತರವನ್ನು ಕಂಡುಹಿಡಿಯಲಿಲ್ಲ. ದಯವಿಟ್ಟು ಮಣ್ಣು, ಎರೆವು, ಕೀಟಗಳು ಅಥವಾ ಕಟಾಯಿಸುವ ಬಗ್ಗೆ ಕೇಳಿ."
#     }
#     return defaults.get(dest_lang, defaults["en"])










# #chatbot_model.py
# import os
# import random
# import requests
# import time
# import json

# from dotenv import load_dotenv

# from translator_util import translate_text, detect_language  # your translation helpers
# # from agro_queries import queries


# # ------------------- Load environment -------------------
# load_dotenv()
# OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# # Base URL for OpenRouter
# # OPENROUTER_BASE = "https://openrouter.ai/api/v1/chat/completions"
# OPENROUTER_BASE = "https://openrouter.ai/api/v1"

# # ------------------- Greetings & Farewells -------------------
# greetings = {
#     "en": ["hello", "hi", "hey", "good morning", "good afternoon", "good evening"],
#     "ta": ["வணக்கம்", "ஹலோ"],
#     "hi": ["नमस्ते", "हैलो"],
#     "ml": ["ഹലോ", "നമസ്ക്കാരം"],
#     "te": ["హలో", "నమస్తే"],
#     "kn": ["ಹಲೋ", "ನಮಸ್ಕಾರ"]
# }

# greeting_responses = {
#     "en": ["Hello! How can I help you today?", "Hi there! Ask me anything about farming. 🌾"],
#     "ta": ["வணக்கம்! இன்று உங்களுக்கு எவ்வாறு உதவலாம்?"],
#     "hi": ["नमस्ते! खेती के बारे में मुझसे कुछ भी पूछें। 🌱"],
#     "ml": ["ഹലോ! കൃഷിയെ കുറിച്ച് എന്തെങ്കിലും ചോദിക്കാം. 🌿"],
#     "te": ["హలో! వ్యవసాయం గురించి ఏదైనా అడగండి. 🌱"],
#     "kn": ["ಹಲೋ! ಕೃಷಿ ಬಗ್ಗೆ ಏನಾದರೂ ಕೇಳಿ. 🌾"]
# }

# farewells = {
#     "en": ["bye", "goodbye", "see you", "thanks", "thank you"],
#     "ta": ["பிரியாவிடை", "நன்றி"],
#     "hi": ["अलविदा", "धन्यवाद"],
#     "ml": ["വിട", "നന്ദി"],
#     "te": ["వీడ్కోలు", "ధన్యవాదాలు"],
#     "kn": ["ವಿದಾಯ", "ಧನ್ಯವಾದಗಳು"]
# }

# farewell_responses = {
#     "en": ["Goodbye! Happy farming! 🌾", "You're welcome! 😊"],
#     "ta": ["வாழ்த்துகள்! மகிழ்ச்சியான விவசாயம்! 🌾"],
#     "hi": ["अलविदा! खेती में सफलता मिले! 🌱"],
#     "ml": ["വിട! സന്തോഷകരമായ കൃഷി ചെയ്യുക! 🌿"],
#     "te": ["వీడ్కోలు! సంతోషకరమైన వ్యవసాయం! 🌱"],
#     "kn": ["ವಿದಾಯ! ಸಂತೋಷಕರ ಕೃಷಿ! 🌾", "ಸ್ವಾಗತ! 😊"]
# }

# # ------------------- Offline Knowledge Base -------------------
# # Use your previous "queries" dictionary here

# from agro_queries import queries  # ✅ Move that huge dict to agro_queries.py for cleanliness

# # Local simple responses (offline fallback)
# offline_responses = {
#     "soil": {
#         # Cereals
#         "cotton": {
#             "en": "Cotton grows best in deep, fertile, well-drained sandy loam soil with good moisture retention.",
#             "ta": "பருத்தி ஆழமான, வளமான, நன்கு வடிகாலமைப்பு கொண்ட மணற்பாங்கு மண்ணில் சிறப்பாக வளரும்.",
#             "hi": "कपास गहरी, उपजाऊ, अच्छी जल निकासी वाली बलुई दोमट मिट्टी में अच्छी तरह उगती है।",
#             "ml": "പഞ്ചു ആഴമുള്ള, വളമുള്ള, നല്ല ഡ്രെയ്‌നേജ് ഉള്ള മണൽ-ചെങ്കല്ല് മണ്ണിൽ വളരുന്നു.",
#             "te": "పత్తి లోతైన, సారవంతమైన, బాగా డ్రైనేజీ ఉన్న ఇసుక లోమ్ మట్టిలో బాగా పెరుగుతుంది.",
#             "kn": "ಹತ್ತಿ ಹಣ್ಣು ಉಗಲು ಉತ್ತಮವಾಗಿ, ಹಣ್ಣಿನತ್ತಿರುವ, ಫಲವತ್ತಾದ, ಚೆನ್ನಾಗಿ ನಿಗದಿತ ಉಪ್ಪಿನ ಮಣ್ಣಿನಲ್ಲಿ ಬೆಳೆಯುತ್ತದೆ."
#         },
#         "rice": {
#             "en": "Rice grows best in clayey loam soil with good water retention.",
#             "ta": "அரிசி நல்ல நீர் தாங்கும் திறன் கொண்ட பஞ்சுப் பாங்கு மண்ணில் சிறப்பாக வளரும்.",
#             "hi": "चावल चिकनी दोमट मिट्टी में सबसे अच्छा उगता है जिसमें पानी की अच्छी धारण क्षमता होती है।",
#             "ml": "അരി നല്ല ജലധാരണമുള്ള മണ്ണിൽ മികച്ചതായി വളരുന്നു.",
#             "te": "బియ్యం మంచి నీరు నిల్వ చేసే మట్టిలో బాగా పెరుగుతుంది.",
#             "kn": "ಅಕ್ಕಿ ಉತ್ತಮವಾಗಿ ಬೆಳೆದಿರಲು, ಮಣ್ಣಿನಲ್ಲಿನ ನೀರಿನ ಉತ್ತಮ ನಿರೋಧಕತೆಯೊಂದಿಗೆ ಮಣ್ಣಿನಲ್ಲಿಯೇ ಬೆಳೆಯುತ್ತದೆ."
#         },
#         "wheat": {
#             "en": "Wheat prefers loamy or alluvial soil with good drainage.",
#             "ta": "கோதுமை நல்ல வடிகாலமைப்பு கொண்ட மணற்பாங்கு மண்ணில் வளரும்.",
#             "hi": "गेहूं अच्छे जल निकासी वाले दोमट या जलोढ़ मिट्टी में उगता है।",
#             "ml": "ഗോതമ്പ് നല്ല ഡ്രെയ്‌നേജ് ഉള്ള മണ്ണിൽ വളരുന്നു.",
#             "te": "గోధుమలు మంచి డ్రైనేజీ ఉన్న లోమ్ మట్టిలో బాగా పెరుగుతాయి.",
#             "kn": "ಗೋಧು ಉತ್ತಮವಾಗಿ ಬೆಳೆಯಲು, ನಿಗದಿತ ಅಥವಾ ನದಿ ತೀರದ ಮಣ್ಣಿನಲ್ಲಿ ಬೆಳೆದು ಬೆಳೆಯುತ್ತದೆ."
#         },
#         "maize": {
#             "en": "Maize grows well in well-drained sandy loam or loamy soil rich in organic matter.",
#             "ta": "சோளம் நன்கு வடிகாலமைப்பு கொண்ட, உயிர்ச்சத்து நிறைந்த மணற்பாங்கு மண்ணில் வளரும்.",
#             "hi": "मक्का अच्छी जल निकासी वाली बलुई दोमट मिट्टी में अच्छी तरह उगता है।",
#             "ml": "ചോളം ജൈവവസ്തുക്കളിൽ സമ്പന്നമായ മണ്ണിൽ വളരുന്നു.",
#             "te": "మొక్కజొన్న సేంద్రీయ పదార్థాలతో సమృద్ధిగా ఉన్న మట్టిలో బాగా పెరుగుతుంది.",
#             "kn": "ಮಕ್ಕಾ ಉತ್ತಮವಾಗಿ ಬೆಳೆಯಲು, ನಂದವಾದ, ಜೈವಿಕ ವಸ್ತುಗಳಿಂದ ಸಮೃದ್ಧ ಮಣ್ಣಿನಲ್ಲಿ ಬೆಳೆದು ಬೆಳೆಯುತ್ತದೆ."
#         },

#         # Vegetables
#         "tomato": {
#             "en": "Tomatoes grow best in well-drained, fertile sandy loam soil with pH 6.0–6.8.",
#             "ta": "தக்காளி நன்கு வடிகாலமைப்பு கொண்ட வளமான மணற்பாங்கு மண்ணில் சிறப்பாக வளரும்.",
#             "hi": "टमाटर उपजाऊ बलुई दोमट मिट्टी में अच्छी तरह उगते हैं।",
#             "ml": "തക്കാളി വളമുള്ള മണൽ മണ്ണിൽ മികച്ചതായി വളരുന്നു.",
#             "te": "టమాటాలు మంచి డ్రైనేజీ ఉన్న మట్టిలో బాగా పెరుగుతాయి.",
#             "kn": "ಟೊಮೇಟೋ ಉತ್ತಮವಾಗಿ ಬೆಳೆಯಲು, ಚೆನ್ನಾಗಿ ನಿಗದಿತ, ಫಲವತ್ತಾದ ಉಪ್ಪಿನ ಮಣ್ಣಿನಲ್ಲಿ (pH 6.0–6.8) ಬೆಳೆದು ಬೆಳೆಯುತ್ತದೆ."
#         },
#         "potato": {
#             "en": "Potatoes prefer loose, well-drained loamy soil with good organic content.",
#             "ta": "உருளைக்கிழங்கு உயிர்ச்சத்து நிறைந்த மணற்பாங்கு மண்ணில் வளரும்.",
#             "hi": "आलू उपजाऊ दोमट मिट्टी में अच्छी तरह उगता है।",
#             "ml": "ഉരുളക്കിഴങ്ങ് നല്ല ജൈവവസ്തുക്കളുള്ള മണ്ണിൽ വളരുന്നു.",
#             "te": "బంగాళదుంపలు సేంద్రీయ పదార్థాలతో సమృద్ధిగా ఉన్న మట్టిలో బాగా పెరుగుతాయి.",
#             "kn": "ಆಲೂಗಡ್ಡೆ ಉತ್ತಮವಾಗಿ ಬೆಳೆಯಲು, ನಿಗದಿತ, ಚೆನ್ನಾಗಿ ನಿಗದಿತ, ಜೈವಿಕ ವಸ್ತುಗಳಿಂದ ಸಮೃದ್ಧ ಮಣ್ಣಿನಲ್ಲಿ ಬೆಳೆದು ಬೆಳೆಯುತ್ತದೆ."
#         },
#         "onion": {
#             "en": "Onions require well-drained sandy loam soil with neutral to slightly alkaline pH.",
#             "ta": "வெங்காயம் நன்கு வடிகாலமைப்பு கொண்ட மணற்பாங்கு மண்ணில் வளரும்.",
#             "hi": "प्याज बलुई दोमट मिट्टी में अच्छी तरह उगता है।",
#             "ml": "സവാള മണൽ മണ്ണിൽ മികച്ചതായി വളരുന്നു.",
#             "te": "ఉల్లిపాయలు లోమ్ మట్టిలో బాగా పెరుగుతాయి.",
#             "kn": "ಈರುಳ್ಳಿ ಉತ್ತಮವಾಗಿ ಬೆಳೆಯಲು, ಚೆನ್ನಾಗಿ ನಿಗದಿತ ಉಪ್ಪಿನ ಮಣ್ಣಿನಲ್ಲಿ, ಸ್ತಿತಿಯಿಂದ ಸ್ವಲ್ಪ ಆಲ್ಕಲೈನ್ pH ಅಗತ್ಯವಿದೆ."
#         },
#         "carrot": {
#             "en": "Carrots grow well in deep, sandy, loose soil to allow root development.",
#             "ta": "காரட் ஆழமான மணற்பாங்கு மண்ணில் சிறப்பாக வளரும்.",
#             "hi": "गाजर रेतीली मिट्टी में अच्छी तरह उगता है।",
#             "ml": "കാരറ്റ് ആഴമുള്ള മണൽ മണ്ണിൽ വളരുന്നു.",
#             "te": "గాజర గడ్డి మట్టిలో బాగా పెరుగుతుంది.",
#             "kn": "ಗಾರ್ಲೆಟ್ ಉತ್ತಮವಾಗಿ ಬೆಳೆಯಲು, ಆಳವಾದ, ನಂದವಾದ, ಬಿಸಿಲು ಮಣ್ಣು, ಬೆಳ್ಳುಳ್ಳಿ ಬೆಳವಣಿಗೆಯನ್ನು ಅನುಮತಿಸುತ್ತದೆ."
#         },

#         # Fruits
#         "mango": {
#             "en": "Mangoes prefer deep, well-drained sandy loam soil rich in organic matter.",
#             "ta": "மாம்பழம் நன்கு வடிகாலமைப்பு கொண்ட வளமான மணற்பாங்கு மண்ணில் வளரும்.",
#             "hi": "आम बलुई दोमट मिट्टी में अच्छी तरह उगता है।",
#             "ml": "മാമ്പഴം വളമുള്ള മണ്ണിൽ വളരുന്നു.",
#             "te": "మామిడి లోమ్ మట్టిలో బాగా పెరుగుతుంది.",
#             "kn": "ಮಾವಿನ ಮರ ಉತ್ತಮವಾಗಿ ಬೆಳೆಯಲು, ಆಳವಾದ, ಚೆನ್ನಾಗಿ ನಿಗದಿತ, ಜೈವಿಕ ವಸ್ತುಗಳಿಂದ ಸಮೃದ್ಧ ಮಣ್ಣಿನಲ್ಲಿ ಬೆಳೆಯುತ್ತದೆ."
#         },
#         "banana": {
#             "en": "Bananas grow best in rich, well-drained loamy soil with high moisture retention.",
#             "ta": "வாழை உயர் ஈரப்பதம் கொண்ட மணற்பாங்கு மண்ணில் வளரும்.",
#             "hi": "केला उपजाऊ दोमट मिट्टी में अच्छी तरह उगता है।",
#             "ml": "വാഴപ്പഴം നല്ല ജലധാരണമുള്ള മണ്ണിൽ വളരുന്നു.",
#             "te": "అరటిపండ్లు లోమ్ మట్టిలో బాగా పెరుగుతాయి.",
#             "kn": "ಬಾಳೆಹಣ್ಣು ಉತ್ತಮವಾಗಿ ಬೆಳೆಯಲು, ಸಮೃದ್ಧ, ಚೆನ್ನಾಗಿ ನಿಗದಿತ ಉಪ್ಪಿನ ಮಣ್ಣು, ಹೆಚ್ಚಿನ ನೀರಿನ ನಿರೋಧಕತೆಯೊಂದಿಗೆ ಬೆಳೆದು ಬೆಳೆಯುತ್ತದೆ."
#         },
#         "apple": {
#             "en": "Apples require well-drained loamy soil with good fertility and slightly acidic pH.",
#             "ta": "ஆப்பிள் நல்ல வடிகாலமைப்பு கொண்ட மணற்பாங்கு மண்ணில் வளரும்.",
#             "hi": "सेब अम्लीय जल निकासी वाली मिट्टी में अच्छी तरह उगते हैं।",
#             "ml": "ആപ്പിൾ നല്ല മണ്ണിൽ വളരുന്നു.",
#             "te": "ఆపిల్ లోమ్ మట్టిలో బాగా పెరుగుతుంది.",
#             "kn": "ಸೇಬು ಉತ್ತಮವಾಗಿ ಬೆಳೆಯಲು, ಚೆನ್ನಾಗಿ ನಿಗದಿತ ಉಪ್ಪಿನ ಮಣ್ಣು, ಉತ್ತಮ ಫಲವತ್ತತೆ ಮತ್ತು ಸ್ವಲ್ಪ ಆಮ್ಲ pH ಅಗತ್ಯವಿದೆ."
#         },
#         "orange": {
#             "en": "Oranges grow best in deep, sandy loam soil with good drainage.",
#             "ta": "ஆரஞ்சு நன்கு வடிகாலமைப்பு கொண்ட மணற்பாங்கு மண்ணில் வளரும்.",
#             "hi": "संतरा गहरी बलुई दोमट मिट्टी में अच्छी तरह उगता है।",
#             "ml": "ഓറഞ്ച് ആഴമുള്ള മണൽ മണ്ണിൽ വളരുന്നു.",
#             "te": "కిర్రిగువ橙 లోమ్ మట్టిలో బాగా పెరుగుతుంది.",
#             "kn": "ಕಿತ್ತಳೆ ಉತ್ತಮವಾಗಿ ಬೆಳೆಯಲು, ಆಳವಾದ, ಚೆನ್ನಾಗಿ ನಿಗದಿತ ಉಪ್ಪಿನ ಮಣ್ಣಿನಲ್ಲಿ ಬೆಳೆದು ಬೆಳೆಯುತ್ತದೆ."
#         },
#         "grape": {
#             "en": "Grapes prefer well-drained, fertile sandy loam soil with moderate pH.",
#             "ta": "திராட்சை வளமான மணற்பாங்கு மண்ணில் வளரும்.",
#             "hi": "अंगूर उपजाऊ दोमट मिट्टी में अच्छी तरह उगते हैं।",
#             "ml": "അങ്ങൂരം വളമുള്ള മണൽ മണ്ണിൽ വളരുന്നു.",
#             "te": "ద్రాక్ష లోమ్ మట్టిలో బాగా పెరుగుతుంది.",
#             "kn": "ದ್ರಾಕ್ಷೆ ಉತ್ತಮವಾಗಿ ಬೆಳೆಯಲು, ಚೆನ್ನಾಗಿ ನಿಗದಿತ, ಫಲವತ್ತಾದ ಉಪ್ಪಿನ ಮಣ್ಣಿನಲ್ಲಿ ಬೆಳೆದು ಬೆಳೆಯುತ್ತದೆ."
#         }
#     },

#     "fertilizer": {
#         "en": [
#             "Use organic compost and nitrogen-rich fertilizer for better yield.",
#             "Phosphorus and potassium fertilizers help root growth.",
#             "Apply balanced NPK fertilizer according to soil test results."
#         ],
#         "ta": ["மேல்தரம் விளைச்சல் பெற உயிர்ச்சத்து நிறைந்த உரம் பயன்படுத்தவும்.", "வேர் வளர்ச்சிக்கு பாஸ்பரஸ் மற்றும் பொட்டாசியம் உரங்கள் உதவும்."],
#         "hi": ["बेहतर उपज के लिए कार्बनिक खाद और नाइट्रोजन-समृद्ध उर्वरक का उपयोग करें।", "जड़ विकास के लिए फॉस्फोरस और पोटेशियम उर्वरक मदद करते हैं।"],
#         "ml": ["മികച്ച വിളവിന് ജൈവ വളവും നൈട്രജൻ സമ്പന്ന വളവും ഉപയോഗിക്കുക."],
#         "te": ["మంచి దిగుబడికి ఆర్గానిక్ కాంపోస్ట్ మరియు నిట్రోజన్-రిచ్ ఎరువులను ఉపయోగించండి."],
#         "kn": ["ಉತ್ತಮ ಫಲಿತಾಂಶಕ್ಕಾಗಿ, ಜೈವಿಕ ರಸ ಮತ್ತು ನೈಟ್ರೋಜನ್-ಸಂಪನ್ನ ಎರೆವುಗಳನ್ನು ಬಳಸಿರಿ.", "ಮೂಲಿಕ ವೃದ್ಧಿಗೆ ಫಾಸ್ಫೋರಸ್ ಮತ್ತು ಪೊಟ್ಯಾಸಿಯಂ ಎರೆವುಗಳು ಸಹಾಯ ಮಾಡುತ್ತವೆ."]
#     },

#     "pest": {
#         "en": [
#             "Neem oil is effective against many pests.",
#             "Use natural pesticides like garlic or chili extracts for eco-friendly farming.",
#             "Regular monitoring and crop rotation help reduce pest attacks."
#         ],
#         "ta": ["நீம் எண்ணெய் பல பூச்சிகளுக்கு விளைவுள்ளது."],
#         "hi": ["नीम का तेल कई कीड़ों के खिलाफ प्रभावी है।"],
#         "ml": ["നീം എണ്ണ പല കീടങ്ങൾക്ക് ഫലപ്രദമാണ്."],
#         "te": ["నీమోయిల్ చాలా pests కు సమర్థవంతంగా పనిచేస్తుంది."],
#         "kn": ["ನೀಮ್ ಎಣ್ಣೆ ಹಲವಾರು ಕೀಟಗಳ ವಿರುದ್ಧ ಪರಿಣಾಮಕಾರಿಯಾಗಿದೆ.", "ಹೆಸರು ಅಥವಾ ಮೆಣಸಿನ ಕಾಳುಗಳಂತಹ ನೈಸರ್ಗಿಕ ಕೀಟನಾಶಕಗಳನ್ನು ಪರಿಸರ ಸ್ನೇಹಿ ಕೃಷಿಗಾಗಿ ಬಳಸಿರಿ.", "ನಿಯಮಿತವಾಗಿ ಮೇಲ್ವಿಚಾರಣೆ ಮತ್ತು ಬೆಳೆ ಬದಲಾವಣೆ ಕೀಟದ ದಾಳಿಗಳನ್ನು ಕಡಿಮೆ ಮಾಡಲು ಸಹಾಯ ಮಾಡುತ್ತದೆ."]
#     },

#     "harvest": {
#         "en": "Harvesting depends on the crop type. Ensure proper maturity before harvesting for best yield.",
#         "ta": "பழங்கள் அறுவடை செய்யும் முன் சரியான வளர்ச்சி பெற்றிருப்பதை உறுதி செய்யுங்கள்.",
#         "hi": "फसल की कटाई प्रकार पर निर्भर करती है। सर्वोत्तम उपज के लिए सही परिपक्वता सुनिश्चित करें।",
#         "ml": "വളവു വിളവെടുപ്പ് വിളയുടെ തരത്തിൽ ആശ്രിതമാണ്. നല്ല വിളവിന് പൂർണമായ വളർച്ച ഉറപ്പാക്കുക.",
#         "te": "ఫలితానికి సరైన పాకవయసు వచ్చి ఉన్నట్లు నిర్ధారించండి.",
#         "kn": "ಹೆಸರು ಬಗೆಯ ಮೇಲೆ ಅವಲಂಬಿತವಾಗಿರುವುದು. ಉತ್ತಮ ಫಲಿತಾಂಶಕ್ಕಾಗಿ, ಕಟಾಯಿಸುವ ಮೊದಲು ಸರಿಯಾದ ಪಾಕವಯಸ್ಸು ಖಚಿತಪಡಿಸಿಕೊಳ್ಳಿ."
#     }
# }

# MAX_RETRIES = 3
# RETRY_DELAY = 2  # seconds between retries


# def safe_request(payload):
#     """Try up to MAX_RETRIES; return response.json() or None on failure."""
#     for attempt in range(1, MAX_RETRIES + 1):
#         try:
#             response = requests.post(
#                 OPENROUTER_BASE,
#                 headers={
#                     "Authorization": f"Bearer {OPENROUTER_API_KEY}",
#                     "Content-Type": "application/json"
#                 },
#                 json=payload,
#                 timeout=15
#             )
#             response.raise_for_status()
#             return response.json()
#         except Exception as e:
#             if attempt < MAX_RETRIES:
#                 print(f"⚠️ Network issue, retrying ({attempt}/{MAX_RETRIES})...")
#                 time.sleep(RETRY_DELAY)
#             else:
#                 print("⚠️ Falling back to offline mode.")
#                 return None

# # ------------------- Offline Response Fetch -------------------
# def get_offline_response(user_input: str, lang="en"):
#     user_input_lower = user_input.lower()
#     for crop, translations in queries.get("soil", {}).items():
#         if crop in user_input_lower:
#             return translations.get(lang, translations.get("en"))
#     for topic in ["fertilizer", "pest", "harvest"]:
#         topic_resp = queries.get(topic, {})
#         resp = topic_resp.get(lang, topic_resp.get("en"))
#         if any(word in user_input_lower for word in topic_resp.keys()):
#             if isinstance(resp, list):
#                 return random.choice(resp)
#             return resp
#             # return random.choice(resp) if isinstance(resp, list) else resp
#     return None

# # ------------------- DeepSeek via OpenRouter -------------------
# def ask_deepseek_openrouter(user_input: str, lang: str = "en"):
#     """
#     Robust generator that streams DeepSeek output via OpenRouter.
#     If any network/streaming issue occurs, gracefully falls back to offline response.
#     Always yields something readable to the caller.
#     """
#     headers = {
#         "Authorization": f"Bearer {OPENROUTER_API_KEY}",
#         "Content-Type": "application/json",
#     }
#     endpoint = f"{OPENROUTER_BASE}/chat/completions"
#     payload = {
#         "model": "deepseek/deepseek-chat-v3.1:free",
#         "stream": True,  # <-- enable token streaming
#         "messages": [
#             {
#                 "role": "system",
#                 "content": (
#                     "You are an agriculture expert chatbot. "
#                     "Reply concisely in the same language as the user's message. "
#                     "Be clear, factual, and friendly."
#                 ),
#             },
#             {"role": "user", "content": user_input},
#         ],
#     }

#     try:
#         with requests.post(endpoint, headers=headers, json=payload, stream=True, timeout=60) as resp:
#             if resp.status_code != 200:
#                 yield f"[Error {resp.status_code}] Using offline response..."
#                 offline = get_offline_response(user_input, lang)
#                 if offline:
#                     yield offline
#                 return

#             for line in resp.iter_lines():
#                 if not line or line == b"":
#                     continue
#                 if line.startswith(b"data: "):
#                     data_str = line[len(b"data: "):].decode("utf-8")
#                     if data_str.strip() == "[DONE]":
#                         break
#                     try:
#                         data_json = json.loads(data_str)
#                         delta = data_json.get("choices", [{}])[0].get("delta", {}).get("content")
#                         if delta:
#                             yield delta
#                     except json.JSONDecodeError:
#                         continue
#     except requests.exceptions.RequestException as e:
#         yield f"[Network Error: {e}] Falling back to offline data..."
#         offline = get_offline_response(user_input, lang)
#         if offline:
#             yield offline

# # ------------------- Core Processing -------------------
# def process_message(user_input):
#     """
#     Generator that:
#     1️⃣ Checks offline responses first.
#     2️⃣ Yields offline response immediately.
#     3️⃣ Streams online AI response if available.
#     4️⃣ Falls back gracefully to offline if network fails.
#     """
#     lang = detect_language(user_input)
#     lower = user_input.lower()

#     # ---- 1️⃣ Check offline first ----
#     offline_resp = get_offline_response(user_input, lang)
#     if offline_resp:
#         yield f"[OFFLINE]{offline_resp} "

#     # ---- 2️⃣ Try online API (OpenRouter/GPT) ----
#     try:
#         headers = {
#             "Authorization": f"Bearer {OPENROUTER_API_KEY}",
#             "Content-Type": "application/json",
#         }
#         payload = {
#             "model": "openai/gpt-4o-mini",
#             "messages": [
#                 {"role": "system", "content": "You are an agriculture expert assistant. Reply concisely."},
#                 {"role": "user", "content": user_input}
#             ],
#             "stream": True
#         }

#         with requests.post(OPENROUTER_BASE + "/chat/completions", headers=headers, json=payload, stream=True, timeout=15) as r:
#             r.raise_for_status()
#             for line in r.iter_lines():
#                 if line and line.startswith(b"data: "):
#                     chunk = line.decode("utf-8")[6:]
#                     if chunk.strip() == "[DONE]":
#                         break
#                     try:
#                         data = json.loads(chunk)
#                         token = data["choices"][0]["delta"].get("content", "")
#                         if token:
#                             yield token
#                     except Exception:
#                         continue
#                     time.sleep(0.015)
#     except Exception as e:
#         # ---- 3️⃣ Network error → offline fallback ----
#         if not offline_resp:  # only if we didn’t yield offline before
#             fallback = get_offline_response(user_input, lang)
#             if fallback:
#                 yield f"[OFFLINE]{fallback} "
#         yield f"\n[Network Error: {str(e)}] Using offline knowledge."













#chatbot_model.py
import os
import time
import json
import random
import requests

from dotenv import load_dotenv
from translator_util import translate_text, detect_language
from agro_queries import queries

# ------------------- Load environment -------------------
load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE = "https://openrouter.ai/api/v1"

# ------------------- Offline Response -------------------
def get_offline_response(user_input: str, lang="en"):
    """Return a relevant offline response if available."""
    user_input_lower = user_input.lower()
    # Check soil crops first
    for crop, translations in queries.get("soil", {}).items():
        if crop in user_input_lower:
            return translations.get(lang, translations.get("en"))

    # Check fertilizer, pest, harvest topics
    for topic in ["fertilizer", "pest", "harvest", "greeting_responses", "farewell_responses"]:
        topic_resp = queries.get(topic, {})
        if isinstance(topic_resp, dict):
            if any(word in user_input_lower for word in topic_resp.keys()):
                resp = topic_resp.get(lang, topic_resp.get("en"))
                if isinstance(resp, list):
                    return random.choice(resp)
                return resp
        elif isinstance(topic_resp, list):
            return random.choice(topic_resp)

    return None

# ------------------- Online Streaming via OpenRouter -------------------
def ask_openrouter_stream(user_input: str, lang="en", retries=2):
    """
    Generator to stream response from OpenRouter.
    Falls back gracefully to offline if network fails.
    Includes retry logic.
    """
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "deepseek/deepseek-chat-v3.1:free",
        "messages": [
            {"role": "system", "content": "You are an agriculture expert assistant. Reply concisely in the same language as the user."},
            {"role": "user", "content": user_input}
        ],
        "stream": True
    }

    for attempt in range(retries + 1):
        try:
            with requests.post(f"{OPENROUTER_BASE}/chat/completions",
                               headers=headers, json=payload, stream=True, timeout=15) as r:
                r.raise_for_status()
                for line in r.iter_lines():
                    if line and line.startswith(b"data: "):
                        chunk = line.decode("utf-8")[6:]
                        if chunk.strip() == "[DONE]":
                            return
                        try:
                            data = json.loads(chunk)
                            token = data["choices"][0]["delta"].get("content", "")
                            if token:
                                yield token
                        except Exception:
                            continue
                        time.sleep(0.015)
            return
        except Exception:
            if attempt == retries:
                return  # fallback silently to offline
            time.sleep(1)  # small delay before retry

# ------------------- Main Processor -------------------
def process_message(user_input: str):
    """
    Offline-first streaming generator with seamless online merge.
    - Yields offline tokens first (green color marker [OFFLINE])
    - Streams online AI tokens afterward
    """
    lang = detect_language(user_input)
    offline_resp = get_offline_response(user_input, lang)

    # Yield offline response char by char
    if offline_resp:
        for ch in offline_resp + " ":
            yield f"[OFFLINE]{ch}"
            time.sleep(0.01)

    # Online streaming from OpenRouter
    online_streamed = False
    for token in ask_openrouter_stream(user_input, lang):
        online_streamed = True
        yield token

    # Fallback if online fails and offline didn't trigger
    if not online_streamed and not offline_resp:
        fallback = get_offline_response(user_input, lang)
        if fallback:
            for ch in fallback + " ":
                yield f"[OFFLINE]{ch}"
                time.sleep(0.01)
