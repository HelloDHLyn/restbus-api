import logging
from functools import wraps

import os
from flask import jsonify
from sqlalchemy.exc import IntegrityError


handler = logging.FileHandler(os.environ['FLASK_LOG_FILE'])
handler.setFormatter(logging.Formatter('%(asctime)s  [%(levelname)s] %(message)s'))

logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


def json_response(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return jsonify(func(*args, **kwargs))

    return wrapper


def transactional(session):
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                data = func(*args, **kwargs)
                session.commit()

                return data
            except IntegrityError:
                logger.exception('Failed to commit the session.')
                session.rollback()

        return wrapper

    return decorate
