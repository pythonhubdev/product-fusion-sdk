from bcrypt import checkpw, gensalt, hashpw


class HashManager:
    def __init__(self) -> None:
        self.salt = gensalt()

    def hash_password(self, password: str) -> str:
        return hashpw(password.encode(), self.salt).decode()

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        return checkpw(password.encode(), hashed_password.encode())


hash_manager: HashManager = HashManager()
