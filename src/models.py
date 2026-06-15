from sqlalchemy import Column, Integer, String, create_engine, select
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker

DATABASE_URL = "sqlite:///exam.db"

# Подключение
# Формат: mysql+pymysql://пользователь:пароль@хост/
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}, echo=False
)

# Фабрика сессий отдает сессии, используя движок
session_factory = sessionmaker(bind=engine)

# Менеджер сессий — для каждого веб-запроса выделяется своя изолированная сессия
db_session = scoped_session(session_factory)

# Базовый класс для создания моделей (таблиц)
Base = declarative_base()


# Описание таблицы пользователей
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(50), nullable=False)
    role = Column(String(20), default="user", nullable=False)


# Функции для инициализации БД (вызываются в main.py)
def create_db():
    """Создает таблицы в базе данных, если они еще не созданы"""
    Base.metadata.create_all(bind=engine)


def create_default_admin():
    """Создает стандартного администратора при первом запуске"""
    with db_session() as session:
        result = session.execute(
            select(User).where(User.username == "admin")
        ).scalar_one_or_none()

        if not result:
            admin = User(username="admin", password="adminpassword", role="admin")
            session.add(admin)
            session.commit()
