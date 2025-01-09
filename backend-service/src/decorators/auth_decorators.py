from functools import wraps

from flask import request, jsonify

from src.services.user_service import UserService


def auth(user_service: UserService):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            auth_header = request.headers.get("Authorization")

            if not auth_header:
                return jsonify({"error": "Authorization header is missing"}), 401

            parts = auth_header.split()
            if parts[0].lower() != "bearer" or len(parts) != 2:
                return jsonify({"error": "Invalid Authorization header format"}), 401

            token = parts[1]

            try:
                user = user_service.validate_token(token)
                kwargs["user_id"] = int(user["user_id"])
            except ValueError as e:
                return jsonify({"error": str(e)}), 401

            return func(*args, **kwargs)

        return wrapper

    return decorator
