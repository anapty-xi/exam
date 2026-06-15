from sqlalchemy import Column, Integer, String, create_engine, select
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker

# Подключение к MySQL в XAMPP
# Формат: mysql+pymysql://пользователь:пароль@хост/имя_базы
DATABASE_URL = "mysql+pymysql://root:@localhost/college_db"

# Создаем движок
engine = create_engine(DATABASE_URL, echo=False)

session_factory = sessionmaker(
    bind=engine
)  # фабрика сессий отдает сессии использую движок
db_session = scoped_session(
    session_factory
)  # менеджер сессий - каждый запрос своя сессия

# базовый класс для создания моделей (таблиц)
Base = declarative_base()


# описание таблицы пользователей
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(50), nullable=False)
    role = Column(String(20), default='user', nullable=False)


# функции для инициализации БД (вызываются в main.py)
def create_db():
    """Создает таблицы в базе данных, если они еще не созданы"""
    Base.metadata.create_all(bind=engine)


def create_default_admin():
    """Создает стандартного администратора при первом запуске"""
    # Проверяем, есть ли уже пользователи в базе
    with db_session() as session:
        result = session.execute(select(User).where(User.username == 'admin')).scalar_one_or_none()
        if not result:
            admin = User(username='admin', password='adminpassword', role='admin')
            session.add(admin)
            session.commit()
