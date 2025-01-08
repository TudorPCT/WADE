from flask import request

from src.services.parsing_service import ParsingService


class ParsingController:
    def __init__(self, app, parsing_service: ParsingService):
        self.app = app
        self.parsing_service = parsing_service
        self.register_routes()

    def register_routes(self):

        @self.app.route("/parse", methods=["POST"])
        def parse():
            data = request.json
            user_input = data.get("user_input")
            results = self.parsing_service.process_user_input(user_input)
            if not results:
                return "", 204
            return results
