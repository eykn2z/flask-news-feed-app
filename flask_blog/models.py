from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base

from flask_blog import app, db

Engine = create_engine(
    app.config["SQLALCHEMY_DATABASE_URI"], encoding="utf-8", echo=False
)
Base = declarative_base()


class BaseModel:
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())


class User(db.Model, BaseModel):
    __tablename__ = "user"
    subid = Column(String(50), unique=True)
    name = Column(String(50), unique=True, nullable=False)


class WebSite(db.Model, BaseModel):
    __tablename__ = "website"
    name = Column(String(50), unique=True, nullable=False)
    siteurl = Column(String(50))
    feedurl = Column(String(50), nullable=False)

    def __init__(self, url):
        f = feedparser.parse(url)
        if (
            "version" in f.values()
            and f.feed.get(f.feed.title_detail.base, None) == None
        ):
            return
        if ("atom" not in f.version) and ("rss" not in f.version):
            return
        feed = f.feed
        self.name = f.feed.title
        self.siteurl = f.feed.get("id", None)
        self.feedurl = f.feed.get("title_detail.base", url)
        # self.updated_at = time_to_datetime(f.feed.get("updated_parsed", None))

    def __repr__(self):
        return "<Website id:{} sitename:{} siteurl:{} feedurl:{} updated_at:{}>".format(
            self.id, self.name, self.siteurl, self.feedurl, self.updated_at
        )


class Entry(db.Model, BaseModel):
    __tablename__ = "entry"
    title = Column(String(50), unique=True, nullable=False)
    url = Column(String(50), nullable=False)
    sitename = Column(String(50), nullable=False)

    def __init__(self, title, url, sitename, updated_at):
        self.title = title
        self.url = url
        self.sitename = sitename
        self.updated_at = updated_at

    def __repr__(self):
        return "<Entry id:{} title:{} url:{} sitename:{}>".format(
            self.id, self.title, self.url, self.sitename
        )
