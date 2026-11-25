# Module
import json
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

def llm_function(prompt):
    createClient = llm_Api()

    geminiAnswer = createClient.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents=prompt
    ) 

    return geminiAnswer.text

def llm_classifier(prompt):
    createClient = llm_Api()

    geminiAnswer = createClient.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": {
                "type": "OBJECT",
                "properties": {
                    "classify": {
                        "type": "STRING",
                        "enum": [
                            "social",
                            "gratitude",
                            "knowledge"
                        ]
                    }
                },
                "required": ["classify"]
            }
        }
    )

    return json.loads(geminiAnswer.text)

def llm_embedding(data):
    createClient = llm_Api()

    embedding_data = createClient.models.embed_content(
    model="gemini-embedding-2",
    contents=data
    )

    return embedding_data.embeddings[0].values

if __name__ == "__main__":
    pass

