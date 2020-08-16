from flask import Flask, render_template, request, jsonify, abort, redirect, session, url_for #importing flask libraries
import sqlite3 #importing sqlite3 libraries
import json #importing json libraries
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
import app_config
import uuid
import requests
#from msalDef import _load_cache, _save_cache, _build_msal_app, _get_token_from_cache
from msal import ConfidentialClientApplication, PublicClientApplication, SerializableTokenCache

app = Flask(__name__) #initialising server

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///networkData.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config.from_object(app_config) #importing app_config variables

Session(app) #creates an object 'session' that can be used to store dict key/value pairs

db = SQLAlchemy(app) #initialising sqlalchemy

class test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    example = db.Column(db.String)

class resultStorage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String)

db.create_all() #creating all sqlalchemytables

@app.route('/')
def home():
    if not session.get('user'):
        return redirect(url_for("login")) #redirect to login page if auth token isn't had

    x = session['user']
    return render_template('home.html', title = "Home", user=x['name'], account=x['preferred_username']) #else redirect to home page

@app.route('/login')
def login():
    try:
        session["state"] = str(uuid.uuid4()) 
        auth_url = _build_msal_app().get_authorization_request_url( #grabs the created url from the relevant scope, state and url
            app_config.SCOPE,
            state=session["state"],
            redirect_uri=url_for("authorised", _external=True) #after token is got, sends the user to the authorised def()
        )
        #print(url_for("authorised", _external=True))
        #print(auth_url)
    except:
        return render_template(error.html)
    return render_template('login.html', results=auth_url, title = "Login") #parses in the link into msal authentication

@app.route('/tokenGet')
def authorised():
    if request.args['state'] != session.get("state"): #if the request != the uuid generated before, redirect to login page
        return redirect(url_for("login"))
    cache = _load_cache()
    result = _build_msal_app(cache).acquire_token_by_authorization_code(
        request.args['code'],
        scopes=app_config.SCOPE,  #uses the scope from app_config
        redirect_uri=url_for("authorised", _external=True))
    if "error" in result:
        return "Login failure: %s, %s" % (
            result["error"], result.get("error_description")) #error handling
    session["user"] = result.get("id_token_claims") #sets key/value pair in session
    _save_cache(cache)
    return redirect("/")

@app.route('/query')
def queryConstruction():
    token = _get_token_from_cache(app_config.SCOPE)
    if not token:
        return redirect(url_for("login"))
    graph_data = requests.get(
        app_config.ENDPOINT,
        headers = {'Authorization': 'Bearer ' + token['access_token']}).json()
    #print(graph_data)
    x = session['user']
    y = graph_data['value']
    print(y)
    return render_template('queryDisplay.html', title="Query", graph_data=y, user=x['name'])

@app.route('/logout')
def logout():
    if session.get('user'):
        session.clear() #clears any information kept in session so that future logins aren't interfered with.
        return redirect("https://login.microsoftonline.com/common/oauth2/v2.0/logout"
            "?post_logout_redirect_uri=" + url_for("home", _external=True)) #using the microsoft common url to logout
    else:
        return redirect(url_for('login'))

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