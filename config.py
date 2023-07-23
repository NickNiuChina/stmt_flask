class Config(object):
    pass
    # DEBUG = True
    # DEVELOPMENT = True
    # SECRET_KEY = 'do-i-really-need-this'
    # FLASK_HTPASSWD_PATH = '/secret/.htpasswd'
    # FLASK_SECRET = SECRET_KEY
    # DB_HOST = 'database' # a docker link

class ProductionConfig(Config):
    DEVELOPMENT = False
    DEBUG = False
    # SECRET_KEY = "dev"
    SECRET_KEY = "$2b$12$Y0QMIGwksa5OhtOBF9BczuAJ0hYMUv7esEBgMMdAuJ4V.7stwxT9e"
    # MySQL configurations 
    MYSQL_DATABASE_USER="stmtflask"
    MYSQL_DATABASE_PASSWORD = 'stmtflask'
    MYSQL_DATABASE_DB = 'stmtflask'
    MYSQL_DATABASE_HOST = '127.0.0.1'
    SQL_FILE = 'schema.sql'
    VERSION = 'v1.0.0'
    LOGFILE = 'stmt_flask.log'