from starter import db, login_manager
from datetime import datetime
from flask_login import UserMixin
from werkzeug.utils import secure_filename
import os

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#--------------------------------     User    --------------------------------
class User(db.Model, UserMixin):
    __tablename = 'user'

    id = db.Column(db.BigInteger, primary_key=True)
    #username = db.Column(db.String(255),unique=True,nullable=False)
    firstname = db.Column(db.String(255), unique=False, nullable=False)
    lastname = db.Column(db.String(255), unique=False, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), unique=False,nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=True)
    birth_date = db.Column(db.Date, unique=False, nullable=False)
    signup_date = db.Column(db.DateTime, unique=False, nullable=False ,default=datetime.utcnow)
    status = db.Column(db.String(255), unique=False, nullable=False)
    role = db.Column(db.String(255), unique=False, nullable=False,default='user')
    gender = db.Column(db.String(255), unique=False, nullable= False)