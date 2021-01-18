from flask_blog import app
import os

port = int(os.environ.get("port"))

if __name__=='__main__':
    app.run(port=port)
