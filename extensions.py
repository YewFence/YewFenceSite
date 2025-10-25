from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# 初始化扩展实例（不绑定 app）
db = SQLAlchemy()
migrate = Migrate()
