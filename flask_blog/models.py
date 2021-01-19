from datetime import datetime

import feedparser
from sqlalchemy import Column, DateTime, Integer, String, create_engine, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from flask_blog import app, db

Engine = create_engine(
    app.config["SQLALCHEMY_DATABASE_URI"], encoding="utf-8", echo=False
)


class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())


Base = declarative_base(cls=BaseModel)


class User(Base):
    __tablename__ = "user"
    __table_args__ = {'extend_existing': True}
    subid = Column(String(50), unique=True)
    name = Column(String(50), unique=True, nullable=False)


class WebSite(Base):
    __tablename__ = "website"
    __table_args__ = {'extend_existing': True}
    name = Column(String(50), unique=True, nullable=False)
    siteurl = Column(String(50))
    feedurl = Column(String(50), nullable=False)

    def __init__(self, url):
        f = feedparser.parse(url)
        if ("version" in f.values() and f.feed.get(f.feed.title_detail.base, None) is None):
            return
        # if ("atom" not in f.version) and ("rss" not in f.version):
        #     return
        # import requests
        # from bs4 import BeautifulSoup
        # if f.feed.get("title", None):
        #     self.name = f.feed.title
        # else:
        #     r = requests.get(url)
        #     self.name = BeautifulSoup(r.text, "html.parser").title.string
        self.name = f.feed.title
        self.siteurl = f.feed.get("id", None)
        self.feedurl = f.feed.get("title_detail.base", url)
        from flask_blog.utils import create_entries
        create_entries(self, flash_enabled=False)
        # self.updated_at = time_to_datetime(f.feed.get("updated_parsed", None))

    def __repr__(self):
        return "<Website id:{} sitename:{} siteurl:{} feedurl:{} updated_at:{}>".format(
            self.id, self.name, self.siteurl, self.feedurl, self.updated_at
        )


class Entry(Base):
    __tablename__ = "entry"
    __table_args__ = {'extend_existing': True}
    title = Column(String(50), unique=True, nullable=False)
    url = Column(String(50), nullable=False)
    website_id = db.Column(db.Integer, db.ForeignKey('website.id', ondelete='CASCADE'), nullable=False)
    website = db.relationship('WebSite', backref=db.backref('entries', lazy=True))

    def __init__(self, title, url, sitename, updated_at):
        self.title = title
        self.url = url
        self.sitename = sitename
        self.updated_at = updated_at

    def __repr__(self):
        return "<Entry id:{} title:{} url:{} sitename:{}>".format(
            self.id, self.title, self.url, self.sitename
        )
