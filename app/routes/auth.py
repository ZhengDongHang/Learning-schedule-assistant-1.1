from flask import Blueprint, render_template, request, redirect, url_for, session
from app.models.user import insert_user, check_user_credentials
import re
from config import db_config

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        account_number = request.form['account_number']
        password = request.form['password']

        # 后端验证
        if len(name) > 30:
            message = "Name must be 30 characters or less."
        elif not re.match(r'^[A-Za-z0-9]{1,30}$', account_number):
            message = "Account number must be 30 characters or less and contain only letters and numbers."
        elif not re.match(r'^[A-Za-z0-9]{1,20}$', password):
            message = "Password must be 20 characters or less and contain only letters and numbers."
        else:
            message = insert_user(name, account_number, password, db_config)

        return render_template('register.html', message=message)
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        account_number = request.form['account_number']
        password = request.form['password']

        user_info = check_user_credentials(account_number, password, db_config)
        if user_info:
            # 如果账户和密码匹配，将用户信息存储在 session 中
            session['user_name'] = user_info['name']
            session['user_account'] = user_info['account_number']
            # 跳转到用户的个人主页
            return redirect(url_for('main.user_page', user_account=user_info['account_number']))
        else:
            message = "Invalid account number or password."
            return render_template('login.html', message=message)
    return render_template('login.html')