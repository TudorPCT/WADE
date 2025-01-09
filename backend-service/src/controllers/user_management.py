from flask import request

from src.services.user_service import UserService


class UserController:
    def __init__(self, app, user_service: UserService):
        self.app = app
        self.user_service = user_service
        self.register_routes()

    def register_routes(self):
        @self.app.route("/generate-password", methods=["POST"])
        def create_user():
            email = request.json["email"]
            user = self.user_service.generate_password(email)
            return user

        @self.app.route("/auth", methods=["POST"])
        def verify_password():
            email = request.json["email"]
            otp = request.json["otp"]
            jwt = self.user_service.verify_password(email, otp)

            if jwt:
                return {"jwt": jwt}
            return "", 401
