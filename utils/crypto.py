from passlib.context import CryptContext
from typing_extensions import deprecated


class Crypto:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bycrypt"], deprecated="auto")

    def encrypt(self, secret):
        return self.pwd_context.hash(secret)

    def verify(self, secret, hash):
        return self.pwd_context.verify(secret, hash)
