from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from services import UserService
from models import db_session

# создаем Blueprint для маршрутов админки
router = Blueprint('admin_page', __name__)

# автоматически закрываем/очищаем сессию после каждого запроса
@router.teardown_request
def shutdown_session(exception=None):
    db_session.remove()

# маршрут авторизации (Логин)
@router.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = UserService.authenticate_user(username, password)
        if user:
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role # Сохраняем роль в сессию
            
            # Перенаправление в зависимости от роли
            if user.role == 'admin':
                return redirect(url_for('admin_page.admin_panel'))
            else:
                return redirect(url_for('admin_page.success_page'))
        else:
            flash('Неверный логин или пароль!')
            
    return render_template('login.html')

# главная страница админки (Просмотр пользователей)
@router.route('/admin')
def admin_panel():
    if session.get('role') != 'admin':
        flash('Доступ разрешен только администраторам!')
        return redirect(url_for('admin_page.login'))
        
    # Запрашиваем список через сервис
    users = UserService.get_all_users()
    return render_template('admin.html', users=users)

# добавление пользователя
@router.route('/admin/add', methods=['POST'])
def add_user():
    if session.get('role') != 'admin':
        flash('Доступ разрешен только администраторам!')
        return redirect(url_for('admin_page.login'))
        
    username = request.form['username']
    password = request.form['password']
    
    if username and password:
        success = UserService.add_user(username, password)
        if not success:
            flash('Пользователь с таким логином уже существует!')
            
    return redirect(url_for('admin_page.admin_panel'))

# удаление пользователя
@router.route('/admin/delete/<int:user_id>')
def delete_user(user_id):
    if session.get('role') != 'admin':
        flash('Доступ разрешен только администраторам!')
        return redirect(url_for('admin_page.login'))
        
    # Вызываем удаление в сервисе
    UserService.delete_user_by_id(user_id)
    return redirect(url_for('admin_page.admin_panel'))

# выход из аккаунта
@router.route('/logout')
def logout():
    session.clear() 
    return redirect(url_for('admin_page.login'))

# успешный вход для обысного юзера
@router.route('/success')
def success_page():
    if 'username' not in session:
        return redirect(url_for('admin_page.login'))
    return render_template('success.html')
