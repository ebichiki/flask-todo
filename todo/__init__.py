from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
#app.config.from_object('todo.config')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)

import todo.views