'''
Flask 的工厂模式
Created on 2023年8月10日
@author: nick_niu
'''
import os

from flask import Flask
import datetime, time
from myproject import stmt
from flask import session
from flask import g, request
import config
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.wrappers import Response

import logging
from flask_babel import Babel

def create_app(test_config=None):
    """
        创建 Flask APP
        @param test_config:
        @return: flask.app.Flask
        @throws Exception
    """

    app = Flask(__name__, instance_relative_config=True)
    app.config['JSON_AS_ASCII'] = False
    # app.config.from_mapping(
    #     JSON_AS_ASCII = False,
    #     # a default secret that should be overridden by instance config
    #     SECRET_KEY="dev",
    #     # MySQL configurations 
    #     MYSQL_DATABASE_USER="stmtflask",
    #     MYSQL_DATABASE_PASSWORD = 'stmtflask',
    #     MYSQL_DATABASE_DB = 'stmtflask',
    #     MYSQL_DATABASE_HOST = '127.0.0.1'
    # )
    
    app.config.from_object(config.ProductionConfig)
    print("------APP config---------------------------------")
    print(app.config)
    print("------APP config---------------------------------")
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    # i18n config
    
    def get_locale():
    # if a user is logged in, use the locale from the user settings
        user = getattr(g, 'user', None)
        if user is not None:
            return user.locale
        # otherwise try to guess the language from the user accept
        # header the browser transmits.  We support de/fr/en in this
        # example.  The best match wins.
        # print("---------------------: " + request.accept_languages.best_match(['zh', 'en']))
        return request.accept_languages.best_match(['zh', 'en'])

    def get_timezone():
        user = getattr(g, 'user', None)
        if user is not None:
            return user.timezone


    # babel = Babel(app, locale_selector=get_locale, timezone_selector=get_timezone)
    babel = Babel(app, locale_selector=get_locale)

    # ensure the instance folder exists or create it
    # try:
    #     os.makedirs(app.instance_path)
    # except OSError:
    #     pass

    # for reverse proxy
    app.wsgi_app = DispatcherMiddleware(
        Response('Not Found', status=404),
        {'/stmt': app.wsgi_app}
    )

    # hello test page
    @app.route("/hello")
    def hello():
        return "Hello, 中文!"
    
    # logging settings to file
    log_level = logging.INFO
    for handler in app.logger.handlers:
        app.logger.removeHandler(handler)
    root = os.path.dirname(os.path.abspath(__file__))
    print("root dir: " + app.root_path)
    logdir = os.path.join(root, 'logs')
    if not os.path.exists(logdir):
        os.mkdir(logdir)
    # log_file = os.path.join(logdir, 'app.log')
    log_file = app.config['LOGFILE']
    handler = logging.FileHandler(log_file)
    handler.setLevel(log_level)
    # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # logging.Formatter(
    #     fmt='%(asctime)s.%(msecs)03d',
    #     datefmt='%Y-%m-%d,%H:%M:%S'
    # )
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    app.logger.setLevel(log_level)
        
    # session expiration time
    @app.before_request
    def make_session_permanent():
        session.permanent = True
        app.permanent_session_lifetime = datetime.timedelta(minutes=60)
        app.logger.info("Before request logger!!")
    
    # server starttime
    start_datetime = datetime.datetime.now()
    
    # context processors
    @app.context_processor
    def context_processor_func():
        end_datetime = datetime.datetime.now()
        delta = end_datetime - start_datetime
        days = delta.days
        if days < 1:
            days = "<1"
        return dict(
            runningDays = days,
            now = datetime.datetime.now()
            )



    # onlineUsers, not in prod now
    app.onlineUsers = 0
    
    # register the database commands
    from myproject import db

    db.init_app(app)
    
    # test db connect and wait for successful connection
    with app.app_context():
        while True:
            try:
                conn = db.get_db()
                print("--- conn object ---")
                print(conn)
                print("-------------------")
                if conn:
                    break
            except Exception as error:    
                print("Error: Please check the database connections!!")
                print("\t", error)
                print("\tSleep 20s\n")
                time.sleep(20)

    # apply the blueprints to the app
    from myproject import auth


    app.register_blueprint(stmt.bp)
    app.register_blueprint(auth.bp)


    # make url_for('index') == url_for('stmt.index')
    # in another app, you might define a separate main index here with
    # app.route, while giving the stmt blueprint a url_prefix, but for
    # the app the stmt will be the main index
    app.add_url_rule("/", endpoint="index")

    return app
