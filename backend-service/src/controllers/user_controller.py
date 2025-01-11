from flask import request

from src.services.user_service import UserService


class UserController:
    def __init__(self, app, user_service: UserService):
        self.app = app
        self.user_service = user_service
        self.register_routes()

    def register_routes(self):
        @self.app.route("/generate-password", methods=["POST"])
        def generate_password():
            email = request.json["email"]
            status, time = self.user_service.generate_password(email)

            if status == 429:
                return "", 429, {"Retry-After": time}

            return "", status

        @self.app.route("/auth", methods=["POST"])
        def verify_password():
            email = request.json["email"]
            otp = request.json["otp"]
            jwt = self.user_service.verify_password(email, otp)

            if jwt:
                return {"jwt": jwt}
            return "", 401
