from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models.event_model import insert_event
from zhipuai import ZhipuAI
import time

event_bp = Blueprint('event', __name__)


@event_bp.route('/input_event', methods=['GET', 'POST'])
def input_event():
    if request.method == 'POST':
        event_type = request.form['event_type']

        if event_type == 'custom':
            name = request.form['name']
            info = request.form['info']
            start_time = request.form['start_time']
            end_time = request.form['end_time']
            user = session.get('user_account')

            # Debug: Print received data
            print(
                f"Custom event data: name={name}, info={info}, start_time={start_time}, end_time={end_time}, user={user}")

            insert_event(name, info, start_time, end_time, user)
            return redirect(url_for('main.user_page', user_account=user))

        elif event_type == 'placeholder':
            user_text = request.form['text']
            print(user_text)
            try:
                result = process_placeholder_text(user_text)
                print(result)
                # 将处理结果返回到前端以便用户确认或修改
                return render_template('confirm_event.html', result=result, user_text=user_text)
            except Exception as e:
                print(e)
                flash(f"处理文本时出错: {str(e)}")
                return redirect(url_for('event.input_event'))

    return render_template('input_event.html')


@event_bp.route('/confirm_event', methods=['POST'])
def confirm_event():
    action = request.form['action']
    if action == 'confirm':
        try:
            # 提取表单数据
            name = request.form['name']
            info = request.form['info']
            start_time = request.form['start_time']
            end_time = request.form['end_time']
            user = session.get('user_account')
            insert_event(name, info, start_time, end_time, user)
            flash("事件已成功添加！")
            return redirect(url_for('main.user_page', user_account=user))
        except Exception as e:
            flash(f"输入有误: {str(e)}")
            return redirect(url_for('event.input_event'))

    elif action == 'retry':
        user_text = request.form['user_text']
        try:
            result = process_placeholder_text(user_text)
            return render_template('confirm_event.html', result=result, user_text=user_text)
        except Exception as e:
            flash(f"处理文本时出错: {str(e)}")
            return redirect(url_for('event.input_event'))

    elif action == 'manual':
        return render_template('input_event.html')

@event_bp.route('/input_event', methods=['GET', 'POST'])
def process_placeholder_text(text):
    exact_time = time.localtime()
    weekday_index = exact_time.tm_wday
    current_time = f"{time.strftime('%Y-%m-%d %H:%M:%S', exact_time)}"
    content = (f"你是一个信息整理助手。用户输入一段文字，你将其转变为'事件名称','事件介绍'，"
               f"'开始时间(yyyy-mm-dd hh:mm)','结束时间(yyyy-mm-dd hh:mm)'。"
               f"有且仅输出上面四个内容。示例，输入：我将于明天下午一点去和林家博打球，打两个小时。"
               f"输出结果：事件名称：打球; 事件介绍：和林家博下午去打球; "
               f"开始时间：2024-8-26 16:00; 结束时间2024-8-26 18:00。"
               f"当前时间为{current_time},星期{weekday_index}")

    client = ZhipuAI(api_key="0f8f83d4d6cd161c1440a7e0e37f41fe.G4dnGhHLwcgAPo3g")
    response = client.chat.completions.create(
        model="glm-4-0520",
        messages=[
            {"role": "system", "content": content},
            {"role": "user", "content": text}
        ],
        top_p=0.7,
        temperature=0.95,
        max_tokens=1024,
        tools=[{"type": "web_search", "web_search": {"search_result": True}}],
        stream=True
    )
    combined_content = ''
    for trunk in response:
        for choice in trunk.choices:
            combined_content += choice.delta.content
    # 提取 '事件名称', '事件介绍', '开始时间', '结束时间'
    segments = combined_content.split(';')

    name = segments[0].split('：')[1].strip()
    info = segments[1].split('：')[1].strip()
    start_time = segments[2].split('：')[1].strip()
    end_time = segments[3].split('：')[1].strip()
    user = session.get('user_account')

    print(name, info, start_time, end_time, user)
    insert_event(name, info, start_time, end_time, user)

    return {
        'name': name,
        'info': info,
        'start_time': start_time,
        'end_time': end_time
    }