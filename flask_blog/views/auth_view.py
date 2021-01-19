import os
from functools import wraps
from os.path import dirname, join

from dotenv import load_dotenv
from flask import flash, redirect, render_template, request, session, url_for
from flask.json import jsonify
from requests_oauthlib import OAuth2Session

from flask_blog import app, db
from flask_blog.models import User


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kargs):
        if not session.get("logged_in"):
            return redirect(url_for("login"))
        return func(*args, **kargs)

    return wrapper


dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)
# This information is obtained upon registration of a new GitHub
client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")
authorization_base_url = "https://github.com/login/oauth/authorize"
token_url = "https://github.com/login/oauth/access_token"


@app.route("/login")
def login():
    github = OAuth2Session(client_id)
    authorization_url, state = github.authorization_url(authorization_base_url)

    # State is used to prevent CSRF, keep this for later.
    session["oauth_state"] = state
    return redirect(authorization_url)


@app.route("/callback")
def callback():
    github = OAuth2Session(client_id, state=session["oauth_state"])
    token = github.fetch_token(
        token_url, client_secret=client_secret, authorization_response=request.url
    )
    # return jsonify(github.get('https://api.github.com/user').json())
    user_info = github.get("https://api.github.com/user").json()
    session["oauth_token"] = token
    subid: str = "github_{}".format(user_info["id"])
    if not User.query.filter(User.subid == subid).all():
        user = User(subid=subid, name=user_info["login"])
        db.session.add(user)
        db.session.commit()
        db.session.close()
        flash(f'ユーザー：{user_info["login"]}が追加されました。')
    session["logged_in"] = True
    flash("ログインしました")
    return redirect(url_for("index"))
    # return redirect(url_for(".profile"))


@app.route("/profile", methods=["GET"])
def profile():
    """Fetching a protected resource using an OAuth 2 token."""
    github = OAuth2Session(client_id, token=session["oauth_token"])
    return jsonify(github.get("https://api.github.com/user").json())


# @app.route('/login', methods=['GET','POST'])
# def login():
#     if request.method=='POST':
#         if request.form['username']!=app.config['USERNAME']:
#             flash('ユーザ名が異なります')
#         elif request.form['password']!=app.config['PASSWORD']:
#             flash('パスワードが異なります')
#         else:
#             session['logged_in']=True
#             flash('ログインしました')
#             return redirect(url_for('index'))
#     return render_template('login.html')


@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    flash("ログアウトしました")
    return redirect(url_for("index"))


@app.errorhandler(404)
def non_existant_route(error):
    return redirect(url_for("index"))
