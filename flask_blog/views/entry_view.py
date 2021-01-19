from flask import flash, redirect, render_template, request, url_for
from flask_blog import app, db
from flask_blog.models import Entry, WebSite
from flask_blog.utils import create_entries
from flask_blog.views.auth_view import login_required


# Show entries
@app.route("/", defaults={"page": 1})
@app.route("/entries", methods=["GET"], defaults={"page": 1})
@app.route("/entry/<int:page>")
def index(page):
    websites = WebSite.query.all()
    entries = Entry.query.order_by(Entry.updated_at.desc()).paginate(page, per_page=10)
    return render_template("index.html", websites=websites, entries=entries)


# Show add website form
@login_required
@app.route("/website/new")
def show_new():
    return render_template("new.html")


# Post website
@login_required
@app.route("/websites", methods=["POST"])
def add_website():
    try:
        website = WebSite(url=request.form["url"])
        db.session.add(website)
        db.session.commit()
        flash("新しくウェブサイトが追加されました")
    except Exception:
        import traceback

        traceback.print_exc()
        flash("追加エラー")
    finally:
        return redirect(url_for("index"))


# Get entries
@login_required
@app.route("/entries", methods=["POST"])
def get_entry():
    websites = WebSite.query.all()
    create_entries(websites)

    return redirect(url_for("index"))
