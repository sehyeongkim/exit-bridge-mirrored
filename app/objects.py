from config import config_obj


class DatabaseConsts(object):
    # mysql
    MYSQL_HOST = config_obj['mysql']['host']
    MYSQL_PORT = config_obj['mysql']['port']
    MYSQL_USER = config_obj['mysql']['user']
    MYSQL_PASSWORD = config_obj['mysql']['passwd']
    MYSQL_DATABASE = config_obj['mysql']['database']
    MYSQL_SCHEMA = config_obj['mysql']['schema']
    MYSQL_TIMEOUT_MS = float(config_obj['mysql']['timeout_ms'])

    # sqlalchemy
    SA_POOL_SIZE = int(config_obj['sqlalchemy']['pool_size'])
    SA_POOL_RECYCLE = float(config_obj['sqlalchemy']['pool_recycle'])
    SA_POOL_TIMEOUT = float(config_obj['sqlalchemy']['pool_timeout'])
    SA_POOL_MAX_OVERFLOW = int(config_obj['sqlalchemy']['max_overflow'])
