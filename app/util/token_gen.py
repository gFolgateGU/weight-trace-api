import jwt
from datetime import datetime, timedelta

from app import application

def generate_session_token(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    token = jwt.encode(payload, application.secret_key, algorithm=application.crypto_alg)
    return token

def decode_session_token(token):   
    try:
        algorithms = []
        algorithms.append(application.crypto_alg)
        payload = jwt.decode(token, application.secret_key, algorithms=algorithms)
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None