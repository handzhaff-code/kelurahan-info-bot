# Core Mechanism

# Module
from task import answer, relevance_answer, need_to_Clarify
from storage import dict_Loop
from llm import llm_function

# Code

def calculated_score(data, question):

    while True:
        '''list of dictionaries'''
        score_per_id = {}

        '''separating dicts from a list of objects'''
        for article in data:
            matched_word = set()

            for keyword in article.keywords:
                split_keyword = keyword.lower().split()

                '''validating each word from list of question.split()'''
                for word in question.lower().split():

                    '''conditional true statement or false'''
                    if word in split_keyword:
                        matched_word.add(word)

            '''out from keyword and word looping'''            
            score_per_id[article.id] = len(matched_word)

        return score_per_id
    
def rank_Articles(score):
    return sorted(
        score.items(),
        key=lambda item:item[1],
        reverse=True
    )

def get_Top_Candidates(score_Sorted):
    id_candidates = []
    '''[0] is first line of sorted score, [1] is values of IDs key'''
    top_score = score_Sorted[0][1]

    if top_score == 0:
        return "NOT_FOUND", [] 

    for id, score in score_Sorted:
        if score == top_score:
            id_candidates.append(id)

    if len(id_candidates) == 1:
        return "UNIQUE", id_candidates
    elif len(id_candidates) > 1:
        return "AMBIGOUS", id_candidates 

'''main.py doesn't know about relation of retrive,build prompt, and build context'''
'''all flow happend in process Search, main.py is only needed to trigger process search function'''
def process_Search(status, ids, question, data):
    if status == "NOT_FOUND":
        return "Maaf, Pertanyaan anda tidak relevan dengan informasi yang kami punya.. Tolong tanyakan kembali !"

    if status == "UNIQUE":
        Task = answer

        retrived_object = retrive_Article(data, ids)
        string_context = build_Context(retrived_object)

        prompt = build_Prompt(question, string_context, Task)

        response = llm_function(prompt)

        return response
    elif status == "AMBIGOUS":
        Task = need_to_Clarify

        retrived_object = retrive_Article(data, ids)
        string_context = build_Context(retrived_object)

        prompt = build_Prompt(question, string_context, Task)

        response = llm_function(prompt)

        return response
    else:
        return "Processing Failed"
    
def retrive_Article(data, ids):

    retrived = []
    '''data parameter contain object of Article'''
    for article in data:
        if article.id in ids:
            retrived.append(article)

    return retrived

'''question from input user'''
'''context return from build_Context'''
'''task from task.py'''
def build_Prompt(question, context, task):

    instruction = "Jawab pertanyaan sesuai dengan Category dan answer yang tersedia."
    Question = question
    articles_Context = context
    Task = task

    prompt = f'''
INSTRUCTION {instruction},
QUESTION {Question},
CONTEXT {articles_Context},
TASK {Task}'''
    
    return prompt

def build_Context(retrived_data):
    context = ""

    for article in retrived_data:
        context += f'''
Article ID {article.id},
Article Category {article.category},
Article Question {article.question},
Article Answer{article.answer}'''

    return context

"""if __name__ == "__main__":
    object = dict_Loop()
    score_per_id, question = calculated_score(object)

    sorted_rank = rank_Articles(score_per_id)
    status, ids_candidates = get_Top_Candidates(sorted_rank)

    response = process_Search(status, ids_candidates, question, object)

    print(response)"""