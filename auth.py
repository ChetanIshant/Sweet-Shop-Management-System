from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext

# secret & token settings
SECRET_KEY = "SECRET123"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Use pbkdf2_sha256 to avoid depending on the bcrypt package and its 72-byte limit.
# pbkdf2_sha256 is secure for common dev/test usage and works without native bcrypt wheels.
pwd = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def get_password_hash(p: str) -> str:
    return pwd.hash(p)

def verify_password(p: str, h: str) -> bool:
    return pwd.verify(p, h)

def create_access_token(username: str):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": username, "exp": int(expire.timestamp())}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None