from flask import Flask

from src.controllers.parsing_controller import ParsingController

app = Flask(__name__)

parsing_controller = ParsingController(app)

if __name__ == '__main__':
    app.run()
