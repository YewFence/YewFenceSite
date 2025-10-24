from functools import wraps
from flask import session, redirect, url_for


def login_required(f):
    """登录验证装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('auth.login', info='请先登录后再访问'))
        return f(*args, **kwargs)
    return decorated_function
