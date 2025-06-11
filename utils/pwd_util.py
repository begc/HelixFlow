import bcrypt, jwt
from datetime import datetime, timedelta
# Function to hash a password
secret_key = "helixFlowVery666NB"

def hash_password(password: str):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_password


# Function to verify a password
def verify_password(plain_password: str, hashed_password: any) -> bool:
    if isinstance(hashed_password, str):
        hashed_password = hashed_password.encode("utf-8")
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password)

def generate_jwt_token(user_id: str, username: str, secret_key: str, expires_days: int = 7) -> str:
    # 构造Payload（包含用户信息和过期时间）
    payload = {
        "user_id": user_id,
        "username": username,
        "exp": datetime.utcnow() + timedelta(days=expires_days)  # 过期时间
    }
    # 生成Token（使用HS256算法）
    token = jwt.encode(payload, secret_key, algorithm="HS256")
    return token
def verify_jwt_token(token: str, secret_key: str) -> dict:
    try:
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise Exception("Token is Expired")
    except jwt.InvalidTokenError:
        raise Exception("Invalid Token")