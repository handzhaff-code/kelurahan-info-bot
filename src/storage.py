import json
import os
import models

# Path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

KNOWLEDGE_JSON = os.path.join(BASE_DIR, "data", "knowledge.json")

def json_Load():
    with open(KNOWLEDGE_JSON, "r", encoding="utf-8") as file:
        file_JSON = json.load(file)
        return file_JSON

def json_Save():
    pass

def dict_Loop():

    resultLoad = json_Load()
    objectResult = []

    for data in resultLoad:
        article = models.Article.from_dict(data)
        objectResult.append(article)

    return objectResult

'''
if __name__ == "__main__":
    hasil = dict_Loop()
    for article in hasil:
        print(article.keywords)'''