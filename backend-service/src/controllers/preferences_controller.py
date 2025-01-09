from flask import request

from src.decorators.auth_decorators import auth
from src.services.preferences_service import PreferencesService
from src.services.user_service import UserService


class PreferencesController:
    def __init__(self, app, preferences_service: PreferencesService, user_service: UserService):
        self.app = app
        self.preferences_service = preferences_service
        self.user_service = user_service
        self.register_routes()

    def register_routes(self):
        @self.app.route("/preferences", methods=["POST"])
        @auth(self.user_service)
        def save_preference(user_id):
            data = request.json
            key = data.get("key")
            value = data.get("value")
            self.preferences_service.save_preference(user_id, key, value)
            return ""

        @self.app.route("/preferences", methods=["DELETE"])
        @auth(self.user_service)
        def delete_preference(user_id):
            data = request.json
            preference_id = int(request.args.get("id"))
            self.preferences_service.delete_preference(preference_id, user_id)
            return ""

        @self.app.route("/preferences", methods=["GET"])
        @auth(self.user_service)
        def get_preferences(user_id):
            preference_key = int(request.args.get("key"))

            if preference_key:
                preferences = self.preferences_service.get_preferences_by_key(preference_key, user_id)
            else:
                preferences = self.preferences_service.get_all_preferences(user_id)

            if not preferences:
                return "", 204

            return [preference.to_json() for preference in preferences]

