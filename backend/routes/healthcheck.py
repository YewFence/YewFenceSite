from flask import Blueprint, jsonify

healthcheck_bp = Blueprint('healthcheck', __name__, url_prefix='/api')


@healthcheck_bp.route('/health')
def health():
    """健康检查路由，只返回简单的状态信息和200状态码"""
    return jsonify({'status': 'ok'}), 200
