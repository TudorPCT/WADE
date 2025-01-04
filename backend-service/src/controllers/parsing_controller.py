from src.services.parsing_service import ParsingService
from flask import request


class ParsingController:
    def __init__(self, app):
        self.app = app
        self.parsing_service = ParsingService("http://localhost:3030/wade/query")
        self.register_routes()

    def register_routes(self):
        @self.app.route("/parse", methods=["GET"])
        def hello():
            return "This is the parsing controller!"

        @self.app.route("/help", methods=["GET"])
        def help():
            return """
                This is the help page for the parsing controller!
                You can use the /parse endpoint to parse user input. 
                - The user input should be sent as a JSON object with a key "user_input".
                - The value of "user_input" should be a string.
                - The response will be a JSON object with the results of parsing the user input.
            """

        @self.app.route("/parse", methods=["POST"])
        def parse():
            data = request.json
            user_input = data.get("user_input")
            results = self.parsing_service.process_user_input(user_input)
            return results
