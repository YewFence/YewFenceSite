from flask import Blueprint

# 导入所有蓝图
from .blog import blog_bp
from .auth import auth_bp
from .crud import crud_bp
from .export import export_bp
from .healthcheck import healthcheck_bp

__all__ = ['blog_bp', 'auth_bp', 'crud_bp', 'export_bp', 'healthcheck_bp']
