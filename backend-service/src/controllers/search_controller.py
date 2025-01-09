from flask import request

from src.services.parsing_service import ParsingService
from src.services.user_service import UserService


class SearchController:
    def __init__(self, app, parsing_service: ParsingService, user_service: UserService):
        self.app = app
        self.parsing_service = parsing_service
        self.user_service = user_service
        self.register_routes()

    def register_routes(self):
        @self.app.route("/search", methods=["POST"])
        def search():
            data = request.json
            user_input = data.get("user_input")
            results = self.parsing_service.process_user_input(user_input)
            if not results:
                return "", 204
            return results
