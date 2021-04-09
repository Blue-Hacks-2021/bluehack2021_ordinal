from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'ordinaldb'

from app import routes

if __name__ == '__main__':
  app.run(debug=True)