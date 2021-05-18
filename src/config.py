import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    ENV = os.getenv("FLASK_ENV")
    PROPAGATE_EXCEPTIONS = os.getenv("PROPAGATE_EXCEPTIONS")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite://")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": os.getenv("POOL_PRE_PING", True),
        "pool_size": os.getenv("POOL_SIZE", 5),
        "pool_recycle": os.getenv("POOL_RECYCLE", 1800),
        "max_overflow": os.getenv("MAX_OVERFLOW", 20),
    }
    SECRET_KEY = os.getenv("SECRET_KEY")
    ACCESS_EXP = int(os.getenv("ACCESS_EXP", '300'))
    REFRESH_EXP = int(os.getenv("REFRESH_EXP", '3600'))
    KONG_URL = os.getenv("KONG_URL")
    KONG_API_KEY = os.getenv("KONG_API_KEY", "")
    MAILER_URL = os.getenv("MAILER_URL")
    KAFKA_URL = os.getenv("KAFKA_URL")
    CLIENT_URL = os.getenv("CLIENT_URL")
    KAFKA_TOPICS = os.getenv("KAFKA_TOPICS").split(",")
    KAFKA_GROUP_ID = os.getenv("KAFKA_GROUP_ID")
    REDIS_CONFIG = {
        'CACHE_TYPE': 'redis',
        'CACHE_REDIS_HOST': os.getenv("CACHE_HOST"),
        'CACHE_REDIS_PORT': os.getenv("CACHE_PORT")
    }
    LOGGING_CONFIG = {
        'version': 1,
        'loggers': {
            '': {  # root logger
                'level': 'NOTSET',
                'handlers': ['debug_coloured_console', 'info_rotating_file_handler', 'error_file_handler'],
            }
        },
        'handlers': {
            'debug_coloured_console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'coloured_console',
                'stream': 'ext://sys.stdout'
            },
            'info_rotating_file_handler': {
                'level': 'INFO',
                'formatter': 'info',
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'filename': 'logs/tapir.log',
                'when': 'D',
                'interval': 1,
                'backupCount': 10
            },
            'error_file_handler': {
                'level': 'WARNING',
                'formatter': 'error',
                'class': 'logging.FileHandler',
                'filename': 'logs/error.log',
                'mode': 'a',
            }
        },
        'formatters': {
            'info': {
                'format': '%(asctime)s [%(levelname)s] %(name)s::%(module)s|%(lineno)s:: %(message)s'
            },
            'debug': {
                'format': '%(asctime)s [%(levelname)s] %(name)s::%(module)s|%(lineno)s:: %(message)s'
            },
            'error': {
                'format': '%(asctime)s [%(levelname)s] %(name)s::%(module)s|%(lineno)s:: %(message)s'
            },
            'coloured_console': {
                '()': 'coloredlogs.ColoredFormatter',
                'format': "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                'datefmt': '%H:%M:%S'
            },
        },
    }
