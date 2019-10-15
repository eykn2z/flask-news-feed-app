from flask_script import Command
from flask_blog import db

class InitDB(Command):#Command実行のためのクラス定義
    "create database"#クラスの説明のためのコメント

    def run(self):
        db.create_all()