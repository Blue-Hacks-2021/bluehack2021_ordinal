from flask import Flask
from config import Config
from flaskext.mysql import MySQL
import re


app = Flask(__name__)
app.config.from_object(Config)

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'ordinaldb'

from app import routes

if __name__ == '__main__':
  app.run(debug=True)