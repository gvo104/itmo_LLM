from models.model_interface import get_access_token, sent_prompt_and_get_response
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def main():

    print("Начало чата")
    access_token = get_access_token()
    while True:
        user_input = input("Вы: ")
        if user_input.lower() in ["exit", "выход", "quit"]:
            print("Выход из GigaChat.")
            break
        
        response = sent_prompt_and_get_response(user_input, access_token)
        print("GigaChat:", response)

if __name__ == "__main__":
    main()