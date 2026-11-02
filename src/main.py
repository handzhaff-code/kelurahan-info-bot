import storage
import pprint
import search
from storage import json_Load
from storage import dict_Loop
from storage import save_offset as sv_offset
from telegram_api import telegram_API
from telegram_api import get_Message
from telegram_api import send_message

def main():
    object_Article = dict_Loop()

    '''telegram API integration'''
    api_keys = telegram_API()
    while True:
        update_id, text, chat_id = get_Message(api_keys)

        score_id = search.calculated_score(object_Article, text)
        sorted_score_id = search.rank_Articles(score_id)
        status, candidates_id = search.get_Top_Candidates(sorted_score_id)

        result = search.process_Search(status, candidates_id, text, object_Article)

        response = send_message(chat_id, result, api_keys)

        if response.get("ok"):
            sv_offset(update_id + 1)
            print(f"Updated ID {update_id}")

if __name__ == "__main__":
    main()

