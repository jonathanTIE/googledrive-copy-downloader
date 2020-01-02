from pydrive.auth import GoogleAuth
import webbrowser

# https://realpython.com/flask-google-login/#creating-a-google-client
from flask import Flask, redirect, request, url_for
from flask_login import LoginManager
from oauthlib.oauth2 import WebApplicationClient
import requests

GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)


class FlaskModified(Flask):
    def run(self, host=None, port=None, debug=None, load_dotenv=True, **options):
        with self.app_context():
            webbrowser.open('https://127.0.0.1:5000') #default url and port for Flask app
            pass
        super(FlaskModified, self).run(host=host, port=port, debug=debug, load_dotenv=load_dotenv, **options)


app = FlaskModified(__name__)

gAuth = GoogleAuth()
auth_url = gAuth.GetAuthUrl()


@app.route("/")
def index():
    return '<a class="button" href="/login">Google Login</a>'


@app.route("/login")
def login():
    return redirect(auth_url)


@app.route("/login/callback")
def callback():
    code = request.args.get("code")
    print("code : " + code)
    gAuth.Auth(code)
    return redirect(url_for("index"))


def auth_and_save_credential():
    app.run(debug="true", ssl_context="adhoc")


#app.run(debug="true", ssl_context="adhoc")
