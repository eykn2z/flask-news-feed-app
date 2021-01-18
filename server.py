from flask_blog import app
import os
import ssl

port = int(os.environ.get("port")) if os.environ.get("port") else 5000

if __name__ == "__main__":
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_cert_chain("ssl/server.crt", "ssl/server.key")
    app.run(
        port=port,
        ssl_context=context,
        threaded=True,
        debug=True,
    )
