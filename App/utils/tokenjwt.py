import jwt
import datetime
from django.conf import settings


def create_access_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + settings.JWT_ACCESS_TOKEN_LIFETIME,
        'type': 'access'
    }
    token = jwt.encode(payload, settings.SECRET_KEY,
                       algorithm=settings.JWT_ALGORITHM)
    return token


def create_refresh_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + settings.JWT_REFRESH_TOKEN_LIFETIME,
        'type': 'refresh'
    }
    token = jwt.encode(payload, settings.SECRET_KEY,
                       algorithm=settings.JWT_ALGORITHM)
    return token


def create_jwt(user_id):

    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=settings.JWT_EXP_DELTA_SECONDS),
    }

    token = jwt.encode(payload, settings.SECRET_KEY,
                       algorithm=settings.JWT_ALGORITHM)

    return token


def verify_jwt(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY,
                             algorithms=[settings.JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
