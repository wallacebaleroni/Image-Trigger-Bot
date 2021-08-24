from flask import Flask, request
import requests
import random
import state
from postgreConnection import *


def main():
    app = Flask(__name__)

    create_database()

    define_routes(app)

    port = os.environ.get('PORT', 5000)
    if port == 5000:
        app.run(debug=True, port=port)
    else:
        app.run(debug=True, host="0.0.0.0", port=port)


def define_routes(app):
    @app.route("/")
    def index():
        return "Hello"

    @app.route("/update", methods=['POST'])
    def update():
        content = request.get_json()

        print("REQUEST:")
        print(request.path)
        print(content)

        if not is_request_valid(content):
            print("NOT VALID MESSAGE")
            return "OK"

        chat_id = content['message']['chat']['id']
        text = content['message']['text']

        print("CHAT_ID="+str(chat_id))
        print("MESSAGE="+text)

        if state.is_setting_keyword:
            set_keyword(text.upper(), chat_id)
            state.is_setting_keyword = False
            send_message(chat_id, "Ok. A palavra chave é " + text + ".")
            return "OK"
        elif state.is_setting_imagerepo:
            set_imagerepo(text, chat_id)
            state.is_setting_imagerepo = False
            send_message(chat_id, "Ok. Repositório setado.")
            return "OK"

        if is_setkeyword_command(content):
            state.is_setting_keyword = True
            send_message(chat_id, "Qual é a palavra?")
            return "OK"
        elif is_setimagerepo_command(content):
            state.is_setting_imagerepo = True
            send_message(chat_id, "Qual o link do repositório?")
            return "OK"

        keyword = get_keyword(chat_id)
        if keyword is None:
            print("KEYWORD NOT SET")
            send_message(chat_id, "A palavra-chave não está definida")
            return "OK"
        print("KEYWORD IS " + keyword)

        if keyword is not None and keyword in text.upper():
            print("KEYWORD FOUND")
            image_url = get_image_from_repo(chat_id)
            if image_url is None:
                print("REPO NOT SET")
                send_message(chat_id, "O repositório não está definido")
                return "OK"
            send_photo(chat_id, image_url)
        else:
            print("KEYWORD NOT FOUND")

        return "OK"

    @app.route("/token", methods=['POST'])
    def set_token():
        content = request.get_json()
        set_telegram_token(content['token'])

        print("SETTING TOKEN")
        print(content['token'])

        return "OK"


def is_request_valid(content):
    if (content is None) or ('message' not in content.keys()) or ('text' not in content['message'].keys()):
        return False
    return True


def is_setkeyword_command(content):
    text = content['message']['text']
    if text.startswith("/setkeyword"):
        return True


def is_setimagerepo_command(content):
    text = content['message']['text']
    if text.startswith("/setimagerepo"):
        return True


def send_message(chat_id, message):
    response = {"chat_id": chat_id, "text": message}
    print("SENDING MESSAGE:")
    print(response)

    token = get_telegram_token()
    if token is None:
        print("COULD NOT GET TOKEN")
        return

    requests.post('https://api.telegram.org/bot' + token + '/sendMessage',
                  json=response)


def send_photo(chat_id, message):
    response = {"chat_id": chat_id, "photo": message}
    print("SENDING PHOTO:")
    print(response)

    token = get_telegram_token()
    if token is None:
        print("COULD NOT GET TOKEN")
        return

    requests.post('https://api.telegram.org/bot' + token + '/sendPhoto',
                  json=response)


def get_image_from_repo(chat_id):
    repo_url = get_imagerepo(chat_id)

    repo_file = requests.get(repo_url)
    repo = repo_file.text.split('\n')

    return random.choice(repo)


main()
