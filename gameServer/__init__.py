from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from gameServer.config import Config
import pymysql
pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

from gameServer import routes
