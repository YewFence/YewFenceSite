import os
from dotenv import load_dotenv

# 加载 .env 文件
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config:
    """基础配置类"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-please-change'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Session 配置（支持前后端分离）
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'  # 允许跨站请求携带 cookie


class DevelopmentConfig(Config):
    """开发环境配置"""
    # 数据库配置，可在环境变量自定义路径
    DATABASE_PATH = os.environ.get('DATABASE_PATH') or '../yewfence_site_data/instance/data.db'
    sql_path = os.path.join(basedir, DATABASE_PATH)
    SQLALCHEMY_DATABASE_URI = ('sqlite:///' + sql_path).replace('\\', '/')
    DEBUG = True
    FLASK_ENV = 'development'
    SESSION_COOKIE_SECURE = False  # 开发环境允许 HTTP


class ProductionConfig(Config):
    """生产环境配置"""
    # 数据库配置，这个是Docker环境下的路径，一般不修改
    sql_path = os.path.join(basedir, 'instance/data.db')
    SQLALCHEMY_DATABASE_URI = ('sqlite:///' + sql_path).replace('\\', '/')
    DEBUG = False
    FLASK_ENV = 'production'
    SESSION_COOKIE_SECURE = False  # Docker 内部使用 HTTP，nginx 处理 HTTPS


# 配置字典
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
