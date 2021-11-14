from passlib.context import CryptContext

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated_method="auto")
pwd_context = CryptContext(schemes=["bcrypt"])

def hash_password(password: str):
    return pwd_context.hash(password)
