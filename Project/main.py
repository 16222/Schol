from flask import Flask, render_template, request, jsonify, abort, redirect, session, url_for #importing flask libraries
import sqlite3 #importing sqlite3 libraries
import json #importing json libraries
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
import app_config
import uuid
#from msalDef import _load_cache, _save_cache, _build_msal_app, _get_token_from_cache
from msal import ConfidentialClientApplication, PublicClientApplication, SerializableTokenCache


app = Flask(__name__) #initialising server

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///networkData.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config.from_object(app_config)

Session(app)

db = SQLAlchemy(app)

class test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    example = db.Column(db.String)

class resultStorage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String)

db.create_all()

@app.route('/')
def home():
    if not session.get('user'):
        return redirect(url_for("login"))
    return render_template('home.html', title = "Home", user=session["user"])

@app.route('/login')
def login():
    session["state"] = str(uuid.uuid4())
    auth_url = _build_msal_app().get_authorization_request_url(
        app_config.SCOPE,
        state=session["state"],
        redirect_uri=url_for("authorised", _external=True)
    )
    print(url_for("authorised", _external=True))
    print(auth_url)
    return render_template('login.html', results=auth_url)

@app.route('/tokenGet')
def authorised():
    if request.args['state'] != session.get("state"):
        return redirect(url_for("login"))
    cache = _load_cache()
    result = _build_msal_app(cache).acquire_token_by_authorization_code(
        request.args['code'],
        scopes=app_config.SCOPE,  # Misspelled scope would cause an HTTP 400 error here
        redirect_uri=url_for("authorised", _external=True))
    if "error" in result:
        return "Login failure: %s, %s" % (
            result["error"], result.get("error_description"))
    session["user"] = result.get("id_token_claims")
    _save_cache(cache)
    return redirect("/home")

@app.route('/query')
def queryConstruction():
    
    return render_template('queryDisplay.html', results=x, title="Query")

@app.route('/getDetails')
def pullDetails():
    return render_template('queryCreation.html')

def _load_cache():
    cache = SerializableTokenCache()
    if session.get("token_cache"):
        cache.deserialize(session["token_cache"])
    return cache

def _save_cache(cache):
    if cache.has_state_changed:
        session["token_cache"] = cache.serialize()

def _build_msal_app(cache=None):
    return ConfidentialClientApplication(
        app_config.CLIENT_ID, authority=app_config.AUTHORITY,
        client_credential=app_config.CLIENT_SECRET, token_cache=cache)

def _get_token_from_cache(scope=None):
    cache = _load_cache()  # This web app maintains one cache per session
    cca = _build_msal_app(cache)
    accounts = cca.get_accounts()
    if accounts:  # So all account(s) belong to the current signed-in user
        result = cca.acquire_token_silent(scope, account=accounts[0])
        _save_cache(cache)
        return result


if __name__ == '__main__':
    app.run(debug=True, host='localhost', port='8080')