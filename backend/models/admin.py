from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db


class Admin(db.Model):
    """管理员模型，存储登录信息"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        """设置密码，存储哈希值到 db"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """检查密码是否正确"""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        """返回字符串表示"""
        return f'<Admin {self.username}>'
