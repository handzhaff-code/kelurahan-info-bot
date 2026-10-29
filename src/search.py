# Core Mechanism

# Module
from storage import dict_Loop

# Code

def search_Article(data):

    while True:
        print("===000===")
        question = input("Masukan pencarian : ").lower().split()

        for article in data:
            for keyword in article.keywords:
                split_keyword = keyword.lower().split()
                for word in question:
                    if word in split_keyword:
                        print("Terdeteksi relevan")
                        print(f"ID Reference {article.id}")
        
        print("===000===")

if __name__ == "__main__":
    object = dict_Loop()
    search_Article(object)