from flask import Flask, render_template, request, jsonify, abort, redirect, session, url_for #importing flask libraries
import sqlite3 #importing sqlite3 libraries
import json #importing json libraries
from flask_sqlalchemy import SQLAlchemy
from msal import PublicClientApplication
from flask_session import Session
import msal
import app_config

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
    return render_template('login.html')

@app.route('/query')
def queryConstruction():
    
    return render_template('queryDisplay.html', results=x, title="Query")

@app.route('/getDetails')
def pullDetails():
    return render_template('queryCreation.html')

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port='8080')