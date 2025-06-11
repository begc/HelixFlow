import json
from fastapi import APIRouter, status, Depends,Response
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth import AuthJWT
from database.base import get_table_session
from router.base import CommonResponse
from database.model.user import UserLogin, UserRegister
from datetime import timedelta
from utils.pwd_util import secret_key,generate_jwt_token
from utils.logger import logger
from service.service_user import register, login
from sqlmodel import Session


router = APIRouter(prefix="/user", tags=["User"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_users(*, user: UserRegister, session: Session = Depends(get_table_session)):

    register_user = register(user=user, session=session)
    return CommonResponse(data=jsonable_encoder(register_user))


@router.post("/login", status_code=status.HTTP_200_OK)
def login_users(*, user: UserLogin, session: Session = Depends(get_table_session), authorize: AuthJWT = Depends()):

    login_user = login(user=user, session=session)
    logger.info(f"login user: {login_user}")



    response =Response("登录成功！")

    response.set_cookie( 'token',
        generate_jwt_token(login_user.id,login_user.name,secret_key=secret_key),
        max_age=24*60*60,
        httponly=True,
        secure=True,
        samesite='Lax')

    return response
@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(authorize: AuthJWT = Depends()):

    response = CommonResponse(data="登出成功")
    return response