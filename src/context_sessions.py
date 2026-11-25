# Library and Modules
import llm
from datetime import datetime, timezone, timedelta
from storage import save_offset
from search import social_prompt, gratitude_prompt
from search import build_context_vector, build_prompt_vector, build_question_prompt
from embeddings import generate_query_embedding, pg_vector_consine_distance
from telegram_api import telegram_API, get_Message, send_message
from datetime import datetime,timezone,timedelta
from pprint import pprint
from connection_dbms import database_connection
import classifier

# Codes 
def main_context_history(api_keys):
    classfy_message = classifier.classify_message_type(api_keys)

    if classfy_message is None:
        return
    
    # Unpacked these values
    update_id, message, chat_id = classfy_message

    # First one we need classify input message from telegram.
    classified_state_dict = classifier.gatekeeper(message)
    classified_state = classified_state_dict["classify"]
    print(classified_state)

    if classified_state == "social":
        prompt = social_prompt(message)
        response = llm.llm_function(prompt)

        response_state = send_message(chat_id, response, api_keys)
        if response_state["ok"] is True:
            save_offset(update_id + 1)
            print("Offset Updated !")
    elif classified_state == "gratitude":
        prompt = gratitude_prompt(message)
        response = llm.llm_function(prompt)

        response_state = send_message(chat_id, response, api_keys)
        if response_state["ok"] is True:
            save_offset(update_id + 1)
            print("Offset Updated !")

    elif classified_state == "knowledge":
        # Lets check status of sessions already exist(active or ended) or none?
        session_id, session_status = generate_sessions(chat_id)

        if session_status == "ended":
            # If its "ended" we should activate their status into "active"
            activate_status(chat_id)

            query = generate_query_embedding(message)
            result_distance = pg_vector_consine_distance(query) # contain list of tuple, we need to choose their distance

            context = build_context_vector(result_distance)
            prompt = build_prompt_vector(message, context)

            response = llm.llm_function(prompt)

            generate_context_history(session_id, message, response) # Put our conversation into the table context_history
            response_state = send_message(chat_id, response, api_keys)

            # If return response json Success dont fotget to update offset state 
            if response_state["ok"] is True:
                save_offset(update_id + 1)
                print("Offset Updated !")

        elif session_status == "active":
            time_now = datetime.now(timezone.utc)
            last_active = last_activity(session_id) # Get the timestempt
            difference = time_now - last_active # Subtraction between now and last activity

            # Filtering the session
            if difference > timedelta(minutes=2):
                deactive_status(chat_id, session_id) # End session at over 2 mins activity sessions

                activate_status(chat_id) # theres delete all_data query at deactive_status(), so i decide to use that only for formality ended session and use delete all data for re
                
                query = generate_query_embedding(message) 
                result_distance = pg_vector_consine_distance(query) # contain list of tuple, we need to choose their distance
                
                context = build_context_vector(result_distance)
                prompt = build_prompt_vector(message, context)
    
                response = llm.llm_function(prompt)
    
                generate_context_history(session_id, message, response) # Put our conversation into the table context_history
                response_state = send_message(chat_id, response, api_keys)

                # If return response json Success dont fotget to update offset state 
                if response_state["ok"] is True:
                    save_offset(update_id + 1)
                    print("Offset Updated !")
            
            elif difference <= timedelta(minutes=2):
                context = all_context(session_id)
                clean_message = build_question_prompt(message, context)
                
                query = generate_query_embedding(clean_message)
                result_distance = pg_vector_consine_distance(query) # contain list of tuple, we need to choose their distance
                                
                context = build_context_vector(result_distance)
                prompt = build_prompt_vector(clean_message, context)
    
                response = llm.llm_function(prompt)
    
                generate_context_history(session_id, message, response) # Put our conversation into the table context_history
                response_state = send_message(chat_id, response, api_keys)

                # If return response json Success dont fotget to update offset state 
                if response_state["ok"] is True:
                    save_offset(update_id + 1)
                    print("Offset Updated !")
    else:
        print("Unknown cls state")
    
def all_context(session_id):
    query = """
    select question, answer
    from context_history
    where session_id = %s
    order by created_at DESC
    limit 3;
    """
    connection = database_connection()
    cursor = connection.cursor()

    cursor.execute(query, (session_id,))
    context_all = cursor.fetchall()

    return context_all

def last_activity(session_id):
    query = """
    select created_at
    from context_history
    where session_id = %s
    order by created_at DESC
    limit 1;
    """
    connection = database_connection()
    cursor = connection.cursor()

    cursor.execute(query, (session_id,))
    context = cursor.fetchone()

    return context[0]

def generate_sessions(chat_id):
    get_status = """
    select session_id, session_status
    from sessions
    where chat_id = %s
    """
    insert_session = """
    insert into sessions(chat_id, session_status, last_activity)
    values(%s, 'ended', DEFAULT)
    returning session_id, session_status
    """
    try:
        connection = database_connection()
        cursor = connection.cursor()

        cursor.execute(get_status, (chat_id,))
        status = cursor.fetchone()

        if status is None:
            cursor.execute(insert_session,(chat_id,))
            updted_status = cursor.fetchone()
            connection.commit()

            sessions_status = updted_status[1]
            session_id = updted_status[0]

            print("Data None")
            return session_id, sessions_status

        sessions_status = status[1]
        session_id = status[0]
        print("Not none")
        return session_id, sessions_status
    
    except Exception:
        connection.rollback()
        raise 

    finally:
        cursor.close()
        connection.close()

def generate_context_history(id, question, answer):
    insert_data = """
    insert into context_history(session_id, question, answer, created_at)
    values(%s, %s, %s, DEFAULT)
    """
    try:
        connection = database_connection()
        cursor = connection.cursor()

        cursor.execute(insert_data, (id, question, answer))

        connection.commit()
        
    except Exception:
        connection.rollback()
        raise
    finally:
        cursor.close()
        connection.close()

def activate_status(chat_id):
    query = """
    UPDATE sessions
    set session_status = 'active',
    last_activity = now()
    where chat_id = %s
    and session_status = 'ended';
    """
    try:
        connection = database_connection()
        cursor = connection.cursor()

        cursor.execute(query,(chat_id,))
        connection.commit()

    except Exception:
        raise
    finally:
        connection.close()

def deactive_status(chat_id, session_id):
    query_end = """
    update sessions 
    set session_status = 'ended',
    last_activity = now()
    where chat_id = %s;
    """

    query_delete_all = """
    delete from context_history
    where session_id = %s;
    """
    try:
        connection = database_connection()
        cursor = connection.cursor()
        cursor.execute(query_end,(chat_id,))
        cursor.execute(query_delete_all,(session_id,))

        connection.commit()
    except Exception:
        raise
    finally:
        cursor.close()
        connection.close()
        
if __name__ == "__main__":
    pass
        