import feedparser

from flask_blog import db
from datetime import datetime

feedMaxCount=3

class WebSite(db.Model):
    __tablename__ = 'websites'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50),unique=True,nullable=False)
    siteurl=db.Column(db.String(50))
    feedurl = db.Column(db.String(50),nullable=False)
    updated=db.Column(db.DateTime)

    def __init__(self, url):
        f = feedparser.parse(url)
        if "version" in f.values() and f.feed.get(f.feed.title_detail.base,None)==None:
            return
        if ("atom" not in f.version) and ("rss" not in f.version):
            return
        feed=f.feed
        self.name = f.feed.title
        self.siteurl = f.feed.get('id',None)
        self.feedurl=f.feed.get('title_detail.base',url)
        self.updated = time_to_datetime(f.feed.get('updated_parsed',None))
        

    def __repr__(self):
        return '<Website id:{} sitename:{} siteurl:{} feedurl:{} updated:{}>'.format(self.id,self.name,self.siteurl,self.feedurl,self.updated)

class Entry(db.Model):
    __tablename__ = 'entries'
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(50),unique=True,nullable=False)
    url = db.Column(db.String(50),nullable=False)
    sitename = db.Column(db.String(50),nullable=False)
    updated = db.Column(db.DateTime)
    
    def __init__(self,title, url,sitename,updated):
        self.title = title
        self.url = url
        self.sitename = sitename
        self.updated = updated

    def __repr__(self):
        return '<Entry id:{} title:{} url:{} sitename:{}>'.format(self.id,self.title,self.url,self.sitename)


def get_feed(website: WebSite) -> WebSite:
    f=feedparser.parse(website.feedurl)
    if f.feed.get('updated_parsed',None)==None:
        return
    if website.updated == time_to_datetime(f.feed.updated_parsed) and Entry.query.filter_by(sitename=website.name).first() is not None:
        return
    entries=[]
    for n,entry in enumerate(f.entries):
        if n>feedMaxCount:
            break
        entries.append(Entry(entry.title,entry.link,website.name,str_to_datetime(entry.updated)))
    return entries


def time_to_datetime(time):
    t=time
    return datetime(t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec)

def str_to_datetime(strtime : str) ->str:
    import re
    day,time,_=re.split('[T|+]',strtime)
    year,mon,mday=map(int,day.split('-'))
    hour,min,sec=map(int,time.split(':'))
    return datetime(year, mon, mday, hour, min, sec)

def get_day_of_week(dt : datetime)-> datetime:
    w_list = ['月', '火', '水', '木', '金', '土', '日']
    return(w_list[dt.weekday()])

def datetime_to_str(dt : datetime)-> datetime:
    return r"{}/{}/{}({}) {}:{}".format(dt.year,dt.month,dt.day,get_day_of_week(dt),dt.hour,dt.minute)