import functools

from flask import Blueprint
from flask import flash, current_app
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from myproject.db import get_db

bp = Blueprint("auth", __name__, url_prefix="/auth")


def login_required(view):
    """View decorator that redirects anonymous users to the login page."""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view


@bp.before_app_request
def load_logged_in_user():
    """If a user id is stored in the session, load the user object from
    the database into ``g.user``."""
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        cur = get_db().cursor()
        cur.execute("SELECT * FROM tb_user WHERE user_id = %s", (user_id,))
        g.user = (
            cur.fetchone()
        )


@bp.route("/register", methods=("GET", "POST"))
def register():
    """Register a new user.

    Validates that the username is not already taken. Hashes the
    password for security.
    """
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None

        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."
        elif (
            db.execute("SELECT id FROM user WHERE username = ?", (username,)).fetchone()
            is not None
        ):
            error = "User {0} is already registered.".format(username)

        if error is None:
            # the name is available, store it in the database and go to
            # the login page
            db.execute(
                "INSERT INTO user (username, password) VALUES (?, ?)",
                (username, generate_password_hash(password)),
            )
            db.commit()
            return redirect(url_for("auth.login"))

        flash(error)

    return render_template("auth/register.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    """Log in a registered user by adding the user id to the session."""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        # if username or password is null or all spaces
        if len(str.strip(username)) ==0 or len(str.strip(password)) == 0:
            return render_template("auth/login.html")           
        
        cur = get_db().cursor()
        error = None
        cur.execute(
            "SELECT * FROM tb_user WHERE username = %s", (username,)
        )
        
        user = cur.fetchone()
        if user is None:
            error = "Username or password is not correct, please check!"
        elif not check_password_hash(user["password"], password):
            error = "Username or password is not correct, please check!"

        if error is None:
            if int(user["status"]) == 2:
                # user has been disabled
                error = "You have been disabled for this site!!"
            else:
                # store the user id in a new session and return to the index
                session.clear()
                session["user_id"] = user["user_id"]
                session["display_name"] = user["display_name"]
                session["username"] = user["username"]

                # online user number +1
                # current_app.onlineUsers += 1 # session scope not correct
                return redirect(url_for("index"))

        flash(error)

    return render_template("auth/login.html")


@bp.route("/logout")
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    # current_app.onlineUsers -= 1 # session scope not correct
    return redirect(url_for("index"))
