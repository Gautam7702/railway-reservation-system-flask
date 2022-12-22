from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///railway.db"
app.config['SECRET_KEY'] = '07c3247f0f4ed891561543db'
db = SQLAlchemy(app) #creates a extension and initialize it with the application
from railway import routes
from railway import models
with app.app_context():
    db.create_all() 


