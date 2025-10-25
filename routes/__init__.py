from flask import Blueprint

# 导入所有蓝图
from .main import main_bp
from .blog import blog_bp
from .auth import auth_bp
from .api import api_bp

__all__ = ['main_bp', 'blog_bp', 'auth_bp', 'api_bp']
