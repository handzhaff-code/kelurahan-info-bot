import storage
import search
from storage import json_Load
from models import Article
import llm


def main():
    '''object result berkaitan dengan storage nanti'''
    objectResult = storage.dict_Loop()
    try:
        Client = llm.llm_Api()
    except ValueError as valErr:
        print(f"error value : {valErr}")

    while True:

        inputUser = input("Masuk sistem (y/n)? ")

        if inputUser.strip() == "y":
            while True:
                questionUser = input("Masukan Pertanyaan = ")

                if len(questionUser) > 20:
                    print("SYSTEM PENGHEMATAN TOKEN DITERAPKAN")
                    print("UNTUK SAAT INI MASUKAN PERTANYAAN DIBAWAH 20 huruf")
                    continue

                try:
                    gemini_result = llm.llm_function(questionUser, Client)

                    print(gemini_result)
                    break
                except Exception as err:
                    print(f"Gagal memberi respon")
                    print(f"Detail error : {err} ")
                    continue

        elif inputUser.strip() == "n":
            break
    
main()

