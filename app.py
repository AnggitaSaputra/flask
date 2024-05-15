from flask import Flask, render_template, request
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'secret123'

# Configuration settings
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flask'

# Initialize MySQL
mysql = MySQL(app)

# Define routes using Flask Blueprints
from routes import auth, main

app.register_blueprint(main)
app.register_blueprint(auth)
