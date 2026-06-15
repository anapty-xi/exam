from sqlalchemy import select
from models import db_session, User

class UserService:
    @staticmethod
    def authenticate_user(username, password) -> User | None:
        """Проверяет логин и пароль. Возвращает пользователя или None."""
        return db_session.execute(
            select(User).where(User.username == username, User.password == password)
        ).scalar_one_or_none()

    @staticmethod
    def get_all_users() -> list[User]:
        """Возвращает список всех зарегистрированных пользователей."""
        return db_session.execute(select(User)).scalars().all()

    @staticmethod
    def add_user(username, password, role='user') -> bool:
        """Безопасно добавляет нового пользователя через транзакцию."""
        with db_session.begin():
            existing = db_session.execute(
                select(User).where(User.username == username)
            ).scalar_one_or_none()
            
            if existing:
                return False 

            new_user = User(username=username, password=password, role=role)
            db_session.add(new_user)
            return True

    @staticmethod
    def delete_user_by_id(user_id) -> bool:
        """Удаляет пользователя по ID"""
        with db_session.begin():
            user = db_session.get(User, user_id)
            db_session.delete(user)
            return True

