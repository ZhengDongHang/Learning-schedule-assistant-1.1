import requests
import pymysql
import pandas as pd
from datetime import datetime, timedelta
from config import db_config

# 爬虫部分
def get_response(week):
    url = "https://ginkgostu.dufe.edu.cn/student/queryCourseList"
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Connection': 'keep-alive',
        'Cookie': 'YourCookieHere',  # 替换为实际的Cookie
        'Host': 'ginkgostu.dufe.edu.cn',
        'Referer': 'https://ginkgostu.dufe.edu.cn/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'batchNo': '10',
        'fingerprint': 'd8a2a587f3eebd8752c043831553e2f5',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': 'Windows',
        'token': 'YourTokenHere',  # 替换为实际的token
    }

    params = {
        'weekNo': week,
    }

    response = requests.get(url, headers=headers, params=params)
    return response

def get_course_data():
    all_data = []

    for week in range(1, 19):
        response = get_response(week)
        if response.status_code == 200:
            try:
                json_data = response.json()
                all_data.append(json_data)
            except ValueError:
                print(f"响应内容不是JSON格式（周次: {week}）")
        else:
            print(f"请求失败，状态码: {response.status_code}（周次: {week}）")

    return all_data

# 数据库部分
def convert_to_datetime(week_day, week_num, time_str, start_date):
    start_date_dt = datetime.strptime(start_date, "%Y-%m-%d")
    start_of_week = start_date_dt - timedelta(days=start_date_dt.weekday())
    target_week_start = start_of_week + timedelta(weeks=week_num - 1)
    target_date = target_week_start + timedelta(days=week_day - 1)

    time_obj = datetime.strptime(time_str, "%H:%M").time()
    result_datetime = datetime.combine(target_date, time_obj)

    return result_datetime.strftime("%Y-%m-%d %H:%M")

def extract_course_data(data, user, startdate):
    extracted_data = []

    for week_data in data:
        for day in week_data['data']:
            for day_list in day['dayList']:
                for course in day_list['courseList']:
                    course_info = {
                        'courseName': course['courseName'],
                        'teacherName': course['teacherName'],
                        'address': course['address'],
                        'dayOfWeek': course['dayOfWeek'],
                        'weekNo': course['weekNo'],
                        'beginTime': convert_to_datetime(int(course['dayOfWeek']), int(course['weekNo']), course['beginTime'], startdate),
                        'endTime': convert_to_datetime(int(course['dayOfWeek']), int(course['weekNo']), course['endTime'], startdate),
                        'user': user
                    }
                    extracted_data.append(course_info)

    df = pd.DataFrame(extracted_data)
    return df

def insert_df_to_sql(df, table_name):
    db_config = {
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'root',
        'passwd': 'passwd', # 替换成实际密码
        'db': 'lsa',
        'charset': 'utf8'
    }

    connection = pymysql.connect(**db_config)

    with connection.cursor() as cursor:
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INT AUTO_INCREMENT PRIMARY KEY,
                courseName VARCHAR(100) NOT NULL,
                teacherName VARCHAR(100) NOT NULL,
                address VARCHAR(255) NOT NULL,
                dayOfWeek INT NOT NULL,
                weekNo INT NOT NULL,
                beginTime DATETIME NOT NULL,
                endTime DATETIME NOT NULL,
                user VARCHAR(100) NOT NULL
            )
        """)

        user_value = df['user'].iloc[0]
        delete_query = f"DELETE FROM {table_name} WHERE user = %s"
        cursor.execute(delete_query, (user_value,))

        insert_query = f"""
            INSERT INTO {table_name} (courseName, teacherName, address, dayOfWeek, weekNo, beginTime, endTime, user)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        for index, row in df.iterrows():
            cursor.execute(insert_query, (
                row['courseName'],
                row['teacherName'],
                row['address'],
                row['dayOfWeek'],
                row['weekNo'],
                row['beginTime'],
                row['endTime'],
                row['user']
            ))

        connection.commit()
        print(f"课表已成功导入 {table_name}.")

    connection.close()

def import_schedule(user, start_date):
    course_data = get_course_data()
    df = extract_course_data(course_data, user, start_date)
    insert_df_to_sql(df, 'courses')


# 获取当前周数
def get_current_week_number():
    # 获取当前日期
    current_date = datetime.now().date()

    # 创建数据库连接
    connection = pymysql.connect(**db_config)

    try:
        with connection.cursor() as cursor:
            # 查询数据库，获取当前日期对应的课程
            query = """
            SELECT weekNo FROM courses 
            WHERE DATE(beginTime) = %s
            ORDER BY beginTime ASC
            LIMIT 1
            """
            cursor.execute(query, (current_date,))
            result = cursor.fetchone()

            if result:
                week_no = result[0]
                return week_no
            else:
                print("没有找到匹配的课程")
                return None
    finally:
        connection.close()


# 数据库查询函数
def get_user_courses(account_number):
    # 连接数据库
    connection = pymysql.connect(**db_config)

    current_week_number = get_current_week_number()
    courses = []

    try:
        with connection.cursor() as cursor:
            # 查询当前用户的课程，当前周的课程
            sql = """
            SELECT courseName, teacherName, address, dayOfWeek, TIME(beginTime) AS beginTime, TIME(endTime) AS endTime
            FROM courses
            WHERE user = %s AND weekNo = %s
            """
            cursor.execute(sql, (account_number, current_week_number))
            courses = cursor.fetchall()
    finally:
        connection.close()

    return courses


