from passlib.context import CryptContext
import logging

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
logging.getLogger('passlib').setLevel(logging.ERROR)         # This is added to silence the passlib error that doesnt break anything


def hash(password: str):
    return pwd_context.hash(password)

def verify(plain_pass, hashed_pass):
    return pwd_context.verify(plain_pass, hashed_pass)