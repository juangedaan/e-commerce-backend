from app.db.models import User
from app.schemas.user import UserCreate


def create_user(user_data: UserCreate, db):
    user = User(username=user_data.username, email=user_data.email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_id(user_id: int, db):
    return db.query(User).filter(User.id == user_id).first()
