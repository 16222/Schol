from flask import Flask, render_template, request, jsonify, abort, redirect #importing flask libraries
import sqlite3 #importing sqlite3 libraries
import json #importing json libraries
import sys, subprocess #importing subprocess and system libraries
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__) #initialising server

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///networkData.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    example = db.Column(db.String)

db.create_all()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/query')
def queryConstruction():
    return render_template('queryCreation.html')

@app.route('/getDetails')
def pullDetails():
    p = subprocess.Popen((["powershell.exe",
                            "./ADFetch.ps1"]),
                             stdout = sys.stdout) #i can execute the powershell script from python

    return render_template('queryDisplay.html')

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port='8080')