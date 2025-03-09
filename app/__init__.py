from flask import Flask

app = Flask(__name__)
app.secret_key = '123456789abcdefg'  # 替换为你自己的密钥

from app.routes.auth import auth_bp
from app.routes.main import main_bp
from app.routes.event import event_bp  # 导入 event_bp
from app.routes.financial_tools import tools_bp


# 注册蓝图
app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)
app.register_blueprint(event_bp, url_prefix='/events')
app.register_blueprint(tools_bp, url_prefix='/tools')