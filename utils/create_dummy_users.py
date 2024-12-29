
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from database import SessionLocal
from user.infra.db_models.user import User
from datetime import datetime
from utils.crypto import Crypto\

crypto = Crypto()
with SessionLocal() as db:
    for i in range(50):
        user = User(
            id=f"UserID-{str(i).zfill(2)}",
            name=f"TestUser{i}",
            email=f"test-user{i}@test.com",
            password=crypto.encrypt(secret="test"),
            memo=None,
            created_at=datetime.now(),
            updated_at=datetime.now(),

        )
        db.add(user)
    db.commit()
