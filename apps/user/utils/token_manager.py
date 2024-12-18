from datetime import datetime, timedelta
from jose import jwt

SECRET_KEY = 'dd9a735175a83222d92c987aec57f4bde11f0e770b5d9ebd5803f734b290edba'
ALGORITHM = "HS256"


def create_token(email: str, user_id: int, expires_delta: timedelta = timedelta(days=60)):
    encode = {
        'email': email,
        'id': user_id
    }
    expires = datetime.utcnow() + expires_delta
    encode.update({
        'exp': expires.timestamp()
    })
    return jwt.encode(
        encode, SECRET_KEY, algorithm=ALGORITHM
    )
