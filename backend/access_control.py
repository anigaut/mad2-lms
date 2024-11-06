from functools import wraps
from flask_jwt_extended import decode_token, get_jwt, verify_jwt_in_request
from flask import jsonify, request


def role_required(role):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims["role"] == role:
                return fn(*args, **kwargs)
            else:
                return jsonify({"message": "You Cannot Access This Page"}), 403
        return decorator
    return wrapper
