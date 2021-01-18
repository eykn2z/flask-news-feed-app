from flask import request, redirect, url_for, render_template, flash, session
from flask_blog import app
from functools import wraps


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kargs):
        if not session.get("logged_in"):
            return redirect(url_for("login"))
        return func(*args, **kargs)

    return wrapper


from requests_oauthlib import OAuth2Session

from flask import Flask, request, redirect, session, url_for
from flask.json import jsonify
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
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
    session["oauth_token"] = token
    return redirect(url_for(".profile"))


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
