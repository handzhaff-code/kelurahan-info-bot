# TESTING API
# Library
import os
import requests
from pprint import pprint
from dotenv import load_dotenv
from storage import load_offset

def telegram_API():
    load_dotenv()

    API_TELEGRAM = os.getenv("TELEGRAM_BOT_TOKEN")

    return API_TELEGRAM

def get_Message(API_key):
    url = f"https://api.telegram.org/bot{API_key}/getUpdates"

    while True:
        try:
            '''this params is variabel'''
            offset = load_offset()
            params = {"timeout" : 30}

            '''this important put params offset into the dict of params for telling telegram to process from offset'''
            '''make offset dictionaries for get params'''
            if offset is not None:
                params["offset"] = offset

            response = requests.get(
                url,
                params= params,
                timeout= 40
            )

            response.raise_for_status()
            data = response.json()

            '''now time to get value from the data'''
            '''if response is none, these iteration will not able running'''
            for update in data["result"]:
                messageUser = None
                updateID = update["update_id"]
                message = update["message"]
                chat = message["chat"]
                chat_id = chat["id"]
                if "text" in message:
                    messagetype = "text"
                    messageUser = message["text"]
                elif "photo" in message:
                    messagetype = "photo"
                elif "video" in message:
                    messagetype = "video"
                elif "document" in message:
                    messagetype = "document"
                else:
                    messagetype = None
                return updateID, messagetype, messageUser, chat_id
        except requests.exceptions.ConnectionError as err:
            print(err)
        except requests.exceptions.Timeout as error:
            print(error)

def send_message(chat_id, message_text, API_key):
    url = f"https://api.telegram.org/bot{API_key}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": message_text
    }

    response = requests.post(url, json=payload)
    response.raise_for_status()

    return response.json()

if __name__ == "__main__":
    pass