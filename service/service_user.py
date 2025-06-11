from database.model.user import User,UserRegister,UserLogin,UserLoginReturn
from sqlmodel import Session,select
from utils.pwd_util import hash_password, verify_password
from fastapi import HTTPException, status

def register(session: Session, user: UserRegister):

    db_user = session.execute(select(User).where(User.name == user.name)).all()

    if db_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="User already exists")
    else:
        try:
            user.password = hash_password(user.password).decode('utf-8')
            db_user = User.from_orm(user)
            session.add(db_user)
            session.commit()
            session.flush()
            session.refresh(db_user)

        except Exception as e:
            session.rollback()
    return db_user


def login(session: Session, user: UserLogin):

    db_user = session.exec(select(User).where(User.name == user.name)).first()

    if not db_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="User doesn't exist")

    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="password doesn't match")
    return UserLoginReturn(name=user.name, id=db_user.id)
