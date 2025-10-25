from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """显示首页"""
    return render_template('index.html')


@main_bp.route('/contact')
def contact():
    """显示联系页"""
    return render_template('contact.html')


@main_bp.route('/interests')
def interests():
    """显示兴趣页"""
    return render_template('interest.html')


@main_bp.route('/about')
def about():
    """显示关于页"""
    return render_template('about.html')
