from fastapi import HTTPException
from jose import jwt
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
import time

from apps.user.models import UserModel
from apps.user.utils.token_manager import SECRET_KEY, ALGORITHM
from config.database_config import db_init


class LoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response: Response = await call_next(request)
        end_time = time.time()

        duration = end_time - start_time
        print(f"Request {request.method} {request.url} took {duration:.4f} seconds")

        return response


class UserHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        token = request.headers.get('Authorization')
        db = db_init()

        if not token:
            raise HTTPException(
                status_code=401,
                detail='Missing Authorization Header'
            )
        try:
            token = token.replace('Bearer ', '')
            payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
            user_id = payload.get('id')
            if not user_id:
                raise HTTPException(
                    status_code=401,
                    detail='Invalid token'
                )
            user: UserModel = db.query(UserModel).filter(UserModel.id == user_id).first()
            if not user:
                raise HTTPException(
                    status_code=401,
                    detail='User not found'
                )
            request.state.user = user
        except Exception:
            raise HTTPException(
                status_code=401,
                detail='Invalid Authorization Header'
            )
