from flask import Flask, request
import os
import requests
import envioronment as env


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

        chat_id = content['message']['chat']['id']
        text = content['message']['text']

        print("CHAT_ID="+str(chat_id))
        print("MESSAGE="+text)

        if env.is_setting_keyword:
            env.keyword = text.upper()
            env.is_setting_keyword = False
            send_message(chat_id, "Ok. A palavra chave é " + text + ".")
            return "OK"

        if is_command(content):
            env.is_setting_keyword = True
            send_message(chat_id, "Qual é a palavra?")
            return "OK"

        if env.keyword is not None and env.keyword in text.upper():
            print("KEYWORD FOUND")
            send_message(chat_id, "Opa")
        else:
            print("KEYWORD NOT FOUND")

        return "OK"


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


main()
