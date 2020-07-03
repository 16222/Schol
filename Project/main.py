from flask import Flask, render_template, request, jsonify, abort, redirect #importing flask libraries
import sqlite3 #importing sqlite3 libraries
import json #importing json libraries
from flask_sqlalchemy import SQLAlchemy

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
    
    return render_template('queryDisplay.html', results=x, title="Query")

@app.route('/getDetails')
def pullDetails():
    return render_template('queryCreation.html')

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port='8080')