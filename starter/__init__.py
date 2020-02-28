#!/usr/bin/python
# coding=utf8

from flask import Flask, Blueprint, render_template
from flask_sqlalchemy import SQLAlchemy
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import babel
import os

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
mysql = MySQL(cursorclass=DictCursor)

#Used when users upload files to your server
UPLOAD_FOLDER = 'static/uploaded_files'

def create_app():
    app = Flask(__name__)
    #Formatting dates in jinja templates
    def format_datetime(value, format='medium'):
        if format == 'full':
            format = "EEEE, d. MMMM y 'at' HH:mm"
        elif format == 'medium':
            format = "dd.MM.y"
        return babel.dates.format_datetime(value, format)
    app.jinja_env.filters['datetime'] = format_datetime

    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:password@localhost/database" #do not forget to replace databse and password
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config['MYSQL_DATABASE_HOST'] = 'localhost'
    app.config['MYSQL_DATABASE_USER'] = 'root'
    app.config['MYSQL_DATABASE_PASSWORD'] = 'password' #do not forget to replace password
    app.config['MYSQL_DATABASE_DB'] = 'database' #do not forget to replace databse

    app.config['SECRET_KEY'] = os.urandom(24)

    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    db.init_app(app)
    mysql.init_app(app)
    bcrypt.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = 'Users.login'
    login_manager.login_message = "Please login to continue" #mesage shows to users who are not looged in if they entered a page that requires login
    login_manager.login_message_category = "danger"

    with app.app_context():
        db.create_all()

    from starter.blueprints.users.routes import Users

    app.register_blueprint(Users)

    return app