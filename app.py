import os
from flask import Flask
from flask_session import Session
from datetime import timedelta


from werkzeug.middleware.proxy_fix import ProxyFix


from blueprints.authenticate import authenticate
from blueprints.landing import landing
from blueprints.visagpt import visagpt
from blueprints.profile import profile

app = Flask(__name__)
app.secret_key = os.urandom(24)

app.config['TEMPLATES_AUTO_RELOAD'] = True
# app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1, x_prefix=1)

app.register_blueprint(authenticate)
app.register_blueprint(landing)
app.register_blueprint(visagpt)
app.register_blueprint(profile)

app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=7)
Session(app)

# app.config.update(
#     SESSION_COOKIE_SECURE=True,
#     SESSION_COOKIE_HTTPONLY=True,
#     SESSION_COOKIE_SAMESITE='Lax',
# )



if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=8080, debug=False)
    app.run(port=8080,debug=True)
