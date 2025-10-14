from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

# ✅ Load OpenRouter API key from .env
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# ✅ Initialize OpenAI client with OpenRouter base URL
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

def ask_deepseek_openrouter(prompt: str):
    try:
        completion = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "http://localhost:5000",  # Or your hosted site
                "X-Title": "AgroChatBot",
            },
            model="deepseek/deepseek-chat-v3.1:free",  # ✅ Current stable public model
            messages=[
                {"role": "system", "content": "You are an agriculture expert helping farmers in simple language."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
        )
        return completion.choices[0].message.content.strip()

    except Exception as e:
        print(f"⚠️ DeepSeek API error: {e}")
        return "Sorry, I couldn’t get a response from DeepSeek right now."

def process_message(user_input):
    response = ask_deepseek_openrouter(user_input)
    return response
