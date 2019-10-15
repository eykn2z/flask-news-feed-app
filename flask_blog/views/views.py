from flask import request,redirect,url_for,render_template,flash,session
from flask_blog import app
from functools import wraps

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return func(*args, **kargs)
    return wrapper


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method=='POST':
        if request.form['username']!=app.config['USERNAME']:
            flash('ユーザ名が異なります')
        elif request.form['password']!=app.config['PASSWORD']:
            flash('パスワードが異なります')
        else:
            session['logged_in']=True
            flash('ログインしました')
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in',None)
    flash('ログアウトしました')
    return redirect(url_for('index'))

@app.errorhandler(404)
def non_existant_route(error):
    return redirect(url_for('index'))




