import os
from flask import Flask, render_template
from config import config
from extensions import db, migrate, cors


def create_app(config_name=None):
    """应用工厂函数"""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')

    app = Flask(__name__)
    app.config.from_object(config.get(config_name, config['default']))

    # 初始化扩展
    db.init_app(app)
    migrate.init_app(app, db)

    # 配置CORS，允许前端访问
    cors.init_app(app, resources={
        r"/*": {
            "origins": ["http://localhost:5173", "http://localhost:3000"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }
    })

    # 注册蓝图
    from routes import main_bp, blog_bp, auth_bp, api_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(blog_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(api_bp)

    # 注册错误处理器
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    # 导入模型（确保迁移能识别）
    with app.app_context():
        from models import Admin, Post

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
