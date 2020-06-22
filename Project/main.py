from flask import Flask, render_template, request, jsonify, abort, redirect #importing flask libraries
import sqlite3 #importing sqlite3 libraries
import json #importing json libraries
import sys, subprocess, os #importing subprocess, system and os libraries
from flask_sqlalchemy import SQLAlchemy
import io #importing i/o libaries

app = Flask(__name__) #initialising server

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///networkData.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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
    return render_template('home.html', title = "Home")

@app.route('/query')
def queryConstruction():
    try:
        p = subprocess.Popen((["powershell.exe",
                                "./query.ps1"]),
                                cwd=os.path.dirname(os.path.realpath(__file__))) 
                                #i can execute the powershell script from python
    finally:
        results = resultStorage.data[0]
    return render_template('queryDisplay.html', results=results, title="Query")

@app.route('/getDetails')
def pullDetails():
    return render_template('queryCreation.html')

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port='8080')