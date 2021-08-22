from flask import Flask, request
import os
import requests
import state


def main():
    app = Flask(__name__)

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

        if is_request_valid(content):
            print("NOT VALID MESSAGE")
            return "OK"

        chat_id = content['message']['chat']['id']
        text = content['message']['text']

        print("CHAT_ID="+str(chat_id))
        print("MESSAGE="+text)

        if state.is_setting_keyword:
            set_keyword(text.upper())
            state.is_setting_keyword = False
            send_message(chat_id, "Ok. A palavra chave é " + text + ".")
            return "OK"

        if is_command(content):
            state.is_setting_keyword = True
            send_message(chat_id, "Qual é a palavra?")
            return "OK"

        keyword = get_keyword()
        if keyword is None:
            print("KEYWORD NOT SET")
            return "OK"
        print("KEYWORD IS " + keyword)

        if keyword is not None and keyword in text.upper():
            print("KEYWORD FOUND")
            send_message(chat_id, "Opa")
        else:
            print("KEYWORD NOT FOUND")

        return "OK"


def is_request_valid(content):
    if (content is None) or ('message' not in content.keys()) or ('text' not in content['message'].keys()):
        return False
    return True


def is_command(content):
    text = content['message']['text']
    if text.startswith("/"):
        return True


def send_message(chat_id, message):
    response = {"chat_id": chat_id, "text": message}
    print("SENDING MESSAGE:")
    print(response)
    requests.post('https://api.telegram.org/bot1919169166:AAGdPZEOYGmqL4HWe1ouKcldFy5yoK_fUq8/sendMessage',
                  json=response)


def set_keyword(keyword):
    filename = "keyword.txt"
    if os.path.exists(filename):
        os.remove(filename)

    f = open(filename, "w")
    f.write(keyword)
    f.close()


def get_keyword():
    filename = "keyword.txt"
    keyword = None

    if os.path.exists(filename):
        f = open(filename, "r")
        keyword = f.read()

    return keyword


main()
