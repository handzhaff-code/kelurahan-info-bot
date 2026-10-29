# Module
import os
from google import genai
from dotenv import load_dotenv

# Code

def llm_Api():
    load_dotenv()

    API_KEY = os.getenv("GEMINI_API_KEY")

    if not API_KEY:
        raise ValueError("API KEY TIDAK DITEMUKAN !")
    
    client = genai.Client(api_key=API_KEY)
    return client

def llm_function(prompt, client):
    geminiAnswer = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents=prompt
    ) 

    return geminiAnswer.text


