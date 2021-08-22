from flask import Flask, request
import os


def main():
    app = Flask(__name__)

    define_routes(app)

    port = os.environ.get('PORT', 5000)
    app.run(host="0.0.0.0", port=port)


def define_routes(app):
    @app.route("/")
    def index():
        return "Hello"

    @app.route("/update", methods=['POST'])
    def update():
        print(request.path)
        print(request.get_json())


main()
