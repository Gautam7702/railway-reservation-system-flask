from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///railway.db"
app.config['SECRET_KEY'] = '07c3247f0f4ed891561543db'
db = SQLAlchemy(app) #creates a extension and initialize it with the application
login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"
from railway import routes
from railway import models
with app.app_context():
    db.create_all() 


