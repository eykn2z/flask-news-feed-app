from flask_blog.models import *

def get_feed(website: WebSite) -> WebSite:
    f = feedparser.parse(website.feedurl)
    if f.feed.get("updated_parsed", None) == None:
        return
    if (
        website.updated == time_to_datetime(f.feed.updated_parsed)
        and Entry.query.filter_by(sitename=website.name).first() is not None
    ):
        return
    entries = []
    for n, entry in enumerate(f.entries):
        if n > feedMaxCount:
            break
        entries.append(
            Entry(entry.title, entry.link, website.name, str_to_datetime(entry.updated))
        )
    return entries


def time_to_datetime(time):
    t = time
    return datetime(t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec)


def str_to_datetime(strtime: str) -> str:
    import re

    day, time, _ = re.split("[T|+]", strtime)
    year, mon, mday = map(int, day.split("-"))
    hour, min, sec = map(int, time.split(":"))
    return datetime(year, mon, mday, hour, min, sec)


def get_day_of_week(dt: datetime) -> datetime:
    w_list = ["月", "火", "水", "木", "金", "土", "日"]
    return w_list[dt.weekday()]


def datetime_to_str(dt: datetime) -> datetime:
    return r"{}/{}/{}({}) {}:{}".format(
        dt.year, dt.month, dt.day, get_day_of_week(dt), dt.hour, dt.minute
    )
