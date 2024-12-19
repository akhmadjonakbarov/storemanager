from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from pydantic import BaseModel, Field
from starlette import status

from apps.user.models import UserModel
from di.db import db_dependency
from core.security import verify_password, get_password_hash, create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

oauth2_bearer = OAuth2PasswordBearer(
    tokenUrl='/api/v1/auth/token',

)


class CreateUserRequest(BaseModel):
    first_name: str = Field(min_length=4)
    last_name: str = Field(min_length=4)
    password: str = Field(min_length=6)
    email: str


class LoginRequest(BaseModel):
    email: str = Field(min_length=6)
    password: str = Field(min_length=6)


@router.post("/login")
async def login(db: db_dependency, login_req: LoginRequest):
    user = db.query(UserModel).filter(login_req.email == UserModel.email and verify_password(
        login_req.password) == UserModel.password).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incorrect username or password"
        )
    return {
        'access_token': create_access_token(
            email=user.email,
            user_id=user.id,
        )
    }


@router.post("/register")
async def register(db: db_dependency, created_user_body: CreateUserRequest):
    try:
        created_user = UserModel(
            email=created_user_body.email,
            first_name=created_user_body.first_name,
            last_name=created_user_body.last_name,
            password=get_password_hash(created_user_body.password)
        )
        db.add(created_user)
        db.commit()
        return {
            "access_token": create_access_token(
                email=created_user.email,
                user_id=created_user.id
            )
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.post("/token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user: UserModel = db.query(UserModel).filter(UserModel.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return {"access_token": create_access_token(user.email, user.id)}
