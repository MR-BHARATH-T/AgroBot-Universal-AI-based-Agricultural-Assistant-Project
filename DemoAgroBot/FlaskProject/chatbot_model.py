# # Chatbot Logic
#
# # Code
#
# import random
#
# # Agriculture chatbot responses (English + Kannada)

# chatbot_model.py
# Agriculture Chatbot Logic with English + Kannada + Auto-detection

import random

# Responses in English + Kannada (paired by index)
responses = {
    "greeting": [
        {
            "en": "Hello! I'm your agriculture assistant. 🌱 How can I help you today?",
            "kn": "ನಮಸ್ಕಾರ! ನಾನು ನಿಮ್ಮ ಕೃಷಿ ಸಹಾಯಕ. 🌱 ನಾನು ಇಂದು ನಿಮಗೆ ಹೇಗೆ ಸಹಾಯ ಮಾಡಬಹುದು?"
        },
        {
            "en": "Hi there! Ask me anything about farming and crops. 🚜",
            "kn": "ಹಾಯ್! ಕೃಷಿ ಮತ್ತು ಬೆಳೆಗಳ ಬಗ್ಗೆ ಏನಾದರೂ ಕೇಳಿ. 🚜"
        }
    ],
    "fertilizer": [
        {
            "en": "For better yield, use organic compost and nitrogen-rich fertilizer like urea. 🌱",
            "kn": "ಉತ್ತಮ ಬೆಳೆಗೆ ಸಾವಯವ ಕಂಪೋಸ್ಟ್ ಮತ್ತು ಯೂರಿಯಾ ಹಾಸು ಗೊಬ್ಬರವನ್ನು ಬಳಸಿ. 🌾"
        },
        {
            "en": "Consider using phosphorus and potassium-based fertilizers for strong root growth. 🌱",
            "kn": "ಬಲವಾದ ಬೇರು ಬೆಳವಣಿಗೆಗೆ ಫಾಸ್ಫರಸ್ ಮತ್ತು ಪೊಟ್ಯಾಸಿಯಂ ಗೊಬ್ಬರಗಳನ್ನು ಬಳಸಿ. 🌾"
        }
    ],
    "pest": [
        {
            "en": "Neem oil spray is effective for many pests. 🐛",
            "kn": "ನೀಮ್ ಎಣ್ಣೆ ಸಿಂಪಡಣೆ ಹಲವಾರು ಕೀಟಗಳ ವಿರುದ್ಧ ಪರಿಣಾಮಕಾರಿ. 🐛"
        },
        {
            "en": "Introduce natural predators like ladybugs to control pest population. 🌱",
            "kn": "ಕೀಟ ನಿಯಂತ್ರಣಕ್ಕಾಗಿ ಲೇಡಿಬಗ್ ಹಾವಿನಂತಹ ಪ್ರಾಕೃತಿಕ ಶತ್ರುಗಳನ್ನು ಪರಿಚಯಿಸಿ. 🌾"
        }
    ],
    "weather": [
        {
            "en": "Please check the local forecast before sowing seeds. ☀️",
            "kn": "ಬೀಜ ಬಿತ್ತುವ ಮೊದಲು ಸ್ಥಳೀಯ ಹವಾಮಾನ ವರದಿ ಪರಿಶೀಲಿಸಿ. 🌧️"
        },
        {
            "en": "Avoid watering plants if heavy rain is predicted. 🌧️",
            "kn": "ಭಾರಿ ಮಳೆಯ ಮುನ್ಸೂಚನೆ ಇದ್ದರೆ ಸಸ್ಯಗಳಿಗೆ ನೀರು ಹಾಕುವುದನ್ನು ತಪ್ಪಿಸಿ. 🌱"
        }
    ],
    "default": [
        {
            "en": "I'm not sure about that. Could you please rephrase? 🤔",
            "kn": "ನನಗೆ ಅದು ಸ್ಪಷ್ಟವಾಗಿಲ್ಲ. ದಯವಿಟ್ಟು ಮತ್ತೆ ವಿವರಿಸಿ? 🤔"
        },
        {
            "en": "Sorry, I don't understand. Can you ask another question? ❓",
            "kn": "ಕ್ಷಮಿಸಿ, ನನಗೆ ಅರ್ಥವಾಗಲಿಲ್ಲ. ಇನ್ನೊಂದು ಪ್ರಶ್ನೆ ಕೇಳಬಹುದೇ? ❓"
        }
    ]
}


# Detect if user input contains Kannada script
def is_kannada(text: str) -> bool:
    return any("\u0c80" <= ch <= "\u0cff" for ch in text)


# Main response function
def get_response(user_input: str) -> str:
    user_input = user_input.lower()

    # Determine category
    if "hi" in user_input or "hello" in user_input or "ನಮಸ್ಕಾರ" in user_input or "ಹಾಯ್" in user_input:
        category = "greeting"
    elif "fertilizer" in user_input or "ಗೊಬ್ಬರ" in user_input:
        category = "fertilizer"
    elif "pest" in user_input or "ಕೀಟ" in user_input:
        category = "pest"
    elif "weather" in user_input or "ಹವಾಮಾನ" in user_input:
        category = "weather"
    else:
        category = "default"

    # Pick a random response
    resp = random.choice(responses[category])

    # Return Kannada or English depending on input
    if is_kannada(user_input):
        return f" ಕನ್ನಡ (Kannada): {resp['kn']}"
    else:
        return f"English: {resp['en']}"





# # Agriculture chatbot responses (English)

# responses = {
#     "greeting": [
#         "Hello! I'm your agriculture assistant. 🌱 How can I help you today?",
#         "Hi there! Ask me anything about farming and crops. 🚜"
#     ],
#     "fertilizer": [
#         "For better yield, use organic compost and nitrogen-rich fertilizer like urea.",
#         "Consider using phosphorus and potassium-based fertilizers for root growth."
#     ],
#     "pest": [
#         "Neem oil spray is effective for many pests.",
#         "Introduce natural predators like ladybugs to control pest population."
#     ],
#     "weather": [
#         "Please check the local forecast before sowing seeds.",
#         "Avoid watering plants if heavy rain is predicted."
#     ],
#     "default": [
#         "I'm not sure about that. Could you please rephrase?",
#         "Sorry, I don't understand. Can you ask another question?"
#     ]
# }
#
# def get_response(user_input):
#     user_input = user_input.lower()
#
#     if "hello" in user_input or "hi" in user_input:
#         return random.choice(responses["greeting"])
#     elif "fertilizer" in user_input:
#         return random.choice(responses["fertilizer"])
#     elif "pest" in user_input:
#         return random.choice(responses["pest"])
#     elif "weather" in user_input:
#         return random.choice(responses["weather"])
#     else:
#         return random.choice(responses["default"])






# # Agriculture chatbot responses (Kannada)

# import random
#
# # Kannada responses
# responses_kn = {
#     "greeting": [
#         "ನಮಸ್ಕಾರ! ನಾನು ನಿಮ್ಮ ಕೃಷಿ ಸಹಾಯಕ. 🌱 ನಾನು ಇಂದು ನಿಮಗೆ ಹೇಗೆ ಸಹಾಯ ಮಾಡಬಹುದು?",
#         "ಹಾಯ್! ಕೃಷಿ ಮತ್ತು ಬೆಳೆಗಳ ಬಗ್ಗೆ ಏನಾದರೂ ಕೇಳಿ. 🚜"
#     ],
#     "fertilizer": [
#         "ಉತ್ತಮ ಬೆಳೆಗೆ, ಜೈವಿಕ ಗೊಬ್ಬರ ಮತ್ತು ಯೂರಿಯಾ ಹೀಗಿನ ನೈಟ್ರೋಜನ್ ಗೊಬ್ಬರವನ್ನು ಬಳಸಿ.",
#         "ಮೂಲಗಳ ಬೆಳವಣಿಗೆಗೆ ಫಾಸ್ಫರಸ್ ಮತ್ತು ಪೊಟ್ಯಾಸಿಯಮ್ ಗೊಬ್ಬರವನ್ನು ಪರಿಗಣಿಸಿ."
#     ],
#     "pest": [
#         "ನೀಮ್ ಎಣ್ಣೆಯ ಸಿಂಪಡಣೆ ಅನೇಕ ಕೀಟಗಳಿಗೆ ಪರಿಣಾಮಕಾರಿ.",
#         "ಕೀಟಗಳ ಸಂಖ್ಯೆಯನ್ನು ನಿಯಂತ್ರಿಸಲು ಲೇಡಿಬಗ್‌ಗಳಂತಹ ನೈಸರ್ಗಿಕ ಪ್ರಾಣಿಗಳನ್ನು ಪರಿಚಯಿಸಿ."
#     ],
#     "weather": [
#         "ಬೀಜ ಬಿತ್ತುವ ಮೊದಲು ದಯವಿಟ್ಟು ಸ್ಥಳೀಯ ಹವಾಮಾನ ವರದಿಯನ್ನು ಪರಿಶೀಲಿಸಿ.",
#         "ಭಾರಿ ಮಳೆ ನಿರೀಕ್ಷೆಯಾದರೆ ಸಸಿಗಳಿಗೆ ನೀರು ಹಾಕಬೇಡಿ."
#     ],
#     "default": [
#         "ನನಗೆ ಖಚಿತವಾಗಿಲ್ಲ. ದಯವಿಟ್ಟು ಪುನಃ ಕೇಳುತ್ತೀರಾ?",
#         "ಕ್ಷಮಿಸಿ, ನನಗೆ ಅರ್ಥವಾಗಲಿಲ್ಲ. ದಯವಿಟ್ಟು ಇನ್ನೊಂದು ಪ್ರಶ್ನೆ ಕೇಳಿ."
#     ]
# }
#
# def get_response_kn(user_input):
#     user_input = user_input.lower()
#     if "ಹಾಯ್" in user_input or "ನಮಸ್ಕಾರ" in user_input:
#         return random.choice(responses_kn["greeting"])
#     elif "ಗೊಬ್ಬರ" in user_input:
#         return random.choice(responses_kn["fertilizer"])
#     elif "ಕೀಟ" in user_input:
#         return random.choice(responses_kn["pest"])
#     elif "ಹವಾಮಾನ" in user_input:
#         return random.choice(responses_kn["weather"])
#     else:
#         return random.choice(responses_kn["default"])



