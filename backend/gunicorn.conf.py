"""Gunicorn 配置文件"""

# 服务器配置
bind = "0.0.0.0:5000"
workers = 4
threads = 2
timeout = 60

# 日志配置
accesslog = "-"  # 输出到 stdout
errorlog = "-"   # 输出到 stderr
loglevel = "info"


class HealthCheckFilter:
    """过滤健康检查请求的日志"""

    def __init__(self, path="/api/health"):
        self.path = path

    def __call__(self, record):
        # 如果请求路径是健康检查端点，则不记录日志
        return self.path not in record.getMessage()


# 应用日志过滤器
logconfig_dict = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "health_check_filter": {
            "()": HealthCheckFilter,
        }
    },
    "formatters": {
        "generic": {
            "format": "%(asctime)s [%(process)d] [%(levelname)s] %(message)s",
            "datefmt": "[%Y-%m-%d %H:%M:%S %z]",
            "class": "logging.Formatter",
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "generic",
            "stream": "ext://sys.stdout",
            "filters": ["health_check_filter"],
        },
        "error_console": {
            "class": "logging.StreamHandler",
            "formatter": "generic",
            "stream": "ext://sys.stderr",
        },
    },
    "root": {"level": "INFO", "handlers": ["console"]},
    "loggers": {
        "gunicorn.error": {
            "level": "INFO",
            "handlers": ["error_console"],
            "propagate": False,
        },
        "gunicorn.access": {
            "level": "INFO",
            "handlers": ["console"],
            "propagate": False,
        },
    },
}
