import os

from flask import Flask
import datetime, time
from myproject import stmt
from flask import session
import config


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
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

    # ensure the instance folder exists or create it
    # try:
    #     os.makedirs(app.instance_path)
    # except OSError:
    #     pass

    # hello test page
    @app.route("/hello")
    def hello():
        return "Hello, 中文!"
    
    # session expiration time
    @app.before_request
    def make_session_permanent():
        session.permanent = True
        app.permanent_session_lifetime = datetime.timedelta(minutes=60)
    
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
