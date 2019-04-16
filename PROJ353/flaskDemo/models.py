from datetime import datetime
from flaskDemo import db, login_manager
from flask_login import UserMixin
from functools import partial
from sqlalchemy import orm, Enum
import enum

db.Model.metadata.reflect(db.engine)

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


class Users(db.Model, UserMixin):
    __table_args__ = {'extend_existing': True}
    userID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable = True)
    address = db.Column(db.String(100))
    password = db.Column(db.String(60), nullable=False)
    def get_id(self):
        return (self.userID)
    def __repr__(self):
        return f"User('{self.username}')"


class Admin(db.Model):
    __table_args__ = {'extend_existing': True}
    adminID = db.Column(db.Integer, primary_key=True)
    def get_id(self):
        return (self.adminID)
    def __repr__(self):
        return f"User('{self.adminID}')"

class category(db.Model):
    __table__ = db.Model.metadata.tables['category']

class products(db.Model):
    __table_args__ = {'extend_existing': True}
    productID = db.Column(db.Integer, primary_key=True)
    productName = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer)
    categoryID = db.Column(db.Integer)
    def get_id(self):
        return (self.productID)
        
    def __repr__(self):
        return f"products('{self.productName}', '{self.price}')"


  
