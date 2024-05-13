from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'secret123'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flask'

mysql = MySQL(app)

from routes import auth, main

app.register_blueprint(main)
app.register_blueprint(auth)
