import datetime
from typing import Optional

from pydantic import BaseModel, validator
from sqlalchemy import Column, BigInteger
from sqlmodel import Field

from database.model.base import SQLModelSerializable


class UserBase(SQLModelSerializable):
    id: Optional[int] = Field(default=None, primary_key=True, description="主键id")
    name: str = Field(unique=True, description="用户名")
    password: str = Field(description="密码")
    nick_name: Optional[str] = Field(description="昵称")
    phone: Optional[str] = Field(description="手机号")
    email: Optional[str] = Field(description="邮箱")
    status: int = Field(default=1, description="状态,1 有效,0 无效")
    remark: Optional[str] = Field(description="备注")
    expire_time: Optional[int] = Field(description="过期时间")
    create_time: Optional[int] = Field(
        sa_column=Column(BigInteger, nullable=False, default=int(datetime.datetime.now().timestamp() * 1000)),
        description="创建时间",
    )
    update_time: Optional[int] = Field(
        sa_column=Column(
            BigInteger, nullable=False,
            default=int(datetime.datetime.now().timestamp() * 1000),
            onupdate=int(datetime.datetime.now().timestamp() * 1000)
        ),
        description="更新时间",
    )

    @validator("name")
    def validate_str(v):
        # dict_keys(['description', 'name', 'id', 'data'])
        if not v:
            raise ValueError("name 不能为空")
        return v


class User(UserBase, table=True):
    __tablename__ = "user"
    __table_args__ = {"comment": "用户表"}


class UserRead(UserBase):
    id: Optional[int]
    role: Optional[str]


class UserQuery(UserBase):
    id: Optional[int]
    name: Optional[str]

class UserLoginReturn(SQLModelSerializable):
    id: Optional[int]
    name: Optional[str]

class UserLogin(BaseModel):
    password: str
    name: str


class UserCreate(UserBase):
    role_id: int


class UserUpdate(UserBase):
    id: int


class UserDelete(SQLModelSerializable):
    id: int
    delete: Optional[int] = 0


class UserRegister(UserBase):
    usergroup_ids: Optional[list[int]] = None

