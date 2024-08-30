from jose import jwt
from datetime import datetime, timedelta, timezone
from app.config import settings


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=30)
    to_encode.update({"exp": expire})
    
    encode_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.HASH_ALGO)
    
    return encode_jwt