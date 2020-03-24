from flask import Flask, render_template, request, jsonify, abort, redirect #importing flask libraries
import sqlite3 #importing sqlite3 libraries
import json #importing json libraries

app = Flask(__name__) #initialising server

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port='8080')