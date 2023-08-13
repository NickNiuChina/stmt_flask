import pymysql
import pymysql.cursors

import click
from flask import current_app
from flask import g
from flask.cli import with_appcontext

def get_db():
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """
    if "db" not in g:
        g.db = pymysql.connect(
            host=current_app.config['MYSQL_DATABASE_HOST'], 
            user=current_app.config['MYSQL_DATABASE_USER'], 
            password=current_app.config['MYSQL_DATABASE_PASSWORD'], 
            database=current_app.config['MYSQL_DATABASE_DB'],
            port=int(current_app.config['MYSQL_DATABASE_PORT']),
            cursorclass=pymysql.cursors.DictCursor
        )
        # g.db.row_factory = MySQL.Row
    return g.db


def close_db(e=None):
    """If this request connected to the database, close the
    connection.
    """
    db = g.pop("db", None)

    if db is not None:
        db.close()

def parse_sql(filename):
    """parse_sql
    To handle sql file, remove the comments and seprate the sql to execute.

    Args:
        filename ( file ): sql file

    Returns:
        list: sql statement
    """
    # data = open(filename, 'r', encoding='utf-8').readlines()
    with current_app.open_resource( filename ) as f:
        # data = f.read().decode("utf8")
        datas = f.readlines()
    stmts = []
    DELIMITER = ';'
    stmt = ''
    data = []
    for item in datas:
        data.append(bytes.decode(item, 'utf-8'))
    
    
    for lineno, line in enumerate(data):
        if not line.strip():
            continue

        if line.startswith('--'):
            continue

        if 'DELIMITER' in line:
            DELIMITER = line.split()[1]
            continue

        if (DELIMITER not in line):
            stmt += line.replace(DELIMITER, ';')
            continue

        if stmt:
            stmt += line
            stmts.append(stmt.strip())
            stmt = ''
        else:
            stmts.append(line.strip())
    return stmts

def init_db():
    """Clear existing data and create new tables."""
    db = get_db()
    
    stmts = parse_sql(current_app.config['SQL_FILE'])
    
    cursor = db.cursor()
    for stmt in stmts:
        cursor.execute(stmt)
    db.commit()
    # http://adamlamers.com/post/GRBJUKCDMPOA



@click.command("init-db")
@with_appcontext
def init_db_command():
    """Clear existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")


def init_app(app):
    """Register database functions with the Flask app. This is called by
    the application factory.
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
