from flask import Flask


def main():
    app = Flask(__name__)
    define_routes(app)
    app.run(debug=True)


def define_routes(app):
    @app.route("/")
    def index():
        return "Hello"


main()
