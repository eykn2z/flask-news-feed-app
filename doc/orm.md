```py
# query取得
from flask_blog.models import *
Website.query.all()

from flask_blog import db
db.session.query(WebSite).all()

# 一括登録

# 削除
db.session.delete(WebSite.query.first())
db.session.commit()
```
