from datetime import datetime, timezone
from passlib.context import CryptContext

def get_current_utc_time():
    return datetime.now(timezone.utc)

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password):
    return bcrypt_context.hash(password)