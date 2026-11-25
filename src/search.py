# Core Mechanism

# Module
from task import ins_Social, ins_memory, ins_Gratitude
from task import instruction as ins
from task import instruction_2 as ins2
from task import answer, relevance_answer, need_to_Clarify, answer_null
from storage import dict_Loop
from llm import llm_function
from task import ins_classification

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
        Task = answer_null
        instruction = ins
        Question = question
    
        prompt = f'''
        INSTRUCTION {instruction},
        QUESTION {Question},
        TASK {Task}'''
        
        response = llm_function(prompt)

        return response

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

    instruction = ins

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

def build_prompt_vector(question, contexts):
    instruction = ins2
    context = contexts

    prompt = f"""
    INSTRUCTION = {instruction}
    USER QUESTION = {question}
    CONTEXT = {context}
    """
    return prompt
    
def build_context_vector(data):
    context = ""

    for e in data:
        context += f"""
Article :{e[0]}
Question :{e[1]}
Answer :{e[2]}
Distance Vector :{e[3]}
"""
    return context

def classifier_context(question):
    instruction = ins_classification
    Question = question

    prompt = f"""
    User Question = {Question},
    follow Instruction = {instruction} 
    """
    return prompt

def build_question_prompt(question, context): # for build question based on memory context
    instruction = ins_memory
    Question = question 
    memory_context = context

    prompt = f"""
    Instruksi wajib = {ins_memory},
    Question Sekarang = {Question},
    Memory context = {memory_context}.
    """

    return prompt

def social_prompt(message):
    ins = ins_Social
    Question = message

    prompt = f"""
    Instruction = {ins},
    Input user = {Question}
    """
    return prompt

def gratitude_prompt(message):
    ins = ins_Gratitude
    Question = message

    prompt = f"""
    Instruction = {ins},
    Input user = {Question}
    """
    return prompt
if __name__ == "__main__":
    pass