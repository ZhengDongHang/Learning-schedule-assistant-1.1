from flask import Blueprint, render_template, session, jsonify, request
import pymysql
from config import db_config
from app.models.course_schedule import get_user_courses


main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    return render_template('index.html')

@main_bp.route('/placeholder')
def placeholder():
    return "<h1>Login Successful</h1>"

@main_bp.route('/user/<string:user_account>')
def user_page(user_account):
    user_account = session.get('user_account', 'Guest')
    return render_template('user_page.html', name=user_account)


@main_bp.route('/tools')
def tools():
    return render_template('tools.html')


@main_bp.route('/import_schedule', methods=['GET', 'POST'])
def import_schedule():
    # 从 session 中获取当前用户的 account_number
    account_number = session.get('user_account')

    if not account_number:
        return jsonify({'error': 'Account number is required'}), 400

    courses = get_user_courses(account_number)

    # 按天分类课程
    schedule_data = {}
    for course in courses:
        day = course[3] # dayOfWeek是元组的第四个

        if day not in schedule_data:
            schedule_data[day] = []
        schedule_data[day].append(course)

    # 定义一个函数，用于将数据中的 timedelta 对象转换为字符串表示
    def convert_schedule_data(data):
        result = []
        for day, events in data.items():
            for event in events:
                course_data = {
                    'course_name': event[0],
                    'teacher_name': event[1],
                    'address': event[2],
                    'dayOfWeek': event[3],
                    'beginTime': str((event[4])),
                    'endTime': str((event[5]))
                }
                result.append(course_data)
        return result

    json_data = convert_schedule_data(schedule_data)
    print(json_data)
    return jsonify(json_data)


