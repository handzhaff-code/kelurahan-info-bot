# Library and module
from telegram_api import send_message, get_Message, telegram_API
from llm import llm_classifier, llm_function
from search import classifier_context
from storage import save_offset

# Code
def gatekeeper(Question):
    prompt = classifier_context(Question)
    classified_state = llm_classifier(prompt) # DICT FORM

    return classified_state

def classify_message_type(api):
    upId, typemessage, messageUser, chatId = get_Message(api)

    # None here mean except != type text, video, and voice.
    if typemessage is None:
        fallback = f"Maaf kami hanya melayani permintaan berbasis text, belum bisa berbentuk {typemessage}"
        fallback_reponse(upId, chatId, fallback, api)
        return None
    
    if typemessage == "text":
        return upId, messageUser, chatId
    elif typemessage == "video":
        fallback = f"Maaf kami hanya melayani permintaan berbasis text, belum bisa berbentuk {typemessage}"
        fallback_reponse(upId, chatId, fallback, api)
        return None
    elif typemessage == "document":
        fallback = f"Maaf kami hanya melayani permintaan berbasis text, belum bisa berbentuk {typemessage}"
        fallback_reponse(upId, chatId, fallback, api)
        return None
    elif typemessage == "photo":
        fallback = f"Maaf kami hanya melayani permintaan berbasis text, belum bisa berbentuk {typemessage}"
        fallback_reponse(upId, chatId, fallback, api)
        return None
    else:
        print(f"Type Message : {typemessage} unknown")

def fallback_reponse(updateId, chatId, fallback, api):
    response = send_message(chatId, fallback, api)

    if response["ok"] is True:
        save_offset(updateId + 1)
        print("update offset")
        
if __name__ == "__main__":
    pass