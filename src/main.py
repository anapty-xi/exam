from flask import Flask

from models import create_db, create_default_admin
from routes import router

# Создаем экземпляр приложения Flask
app = Flask(__name__)
app.secret_key = "secret_key_123"

# регистрируем основной роутер эндпоинтов (блюпринт здесь)
app.register_blueprint(router)

if __name__ == "__main__":
    # Создаем таблицы добавляем первого админа
    create_db()
    create_default_admin()

    # Запускаем сервер
    app.run(debug=True)
