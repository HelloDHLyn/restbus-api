from functools import wraps

from flask import jsonify


def json_response(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return jsonify(func(*args, **kwargs))

    return wrapper
