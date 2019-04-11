from datetime import datetime
from flaskDemo import db, login_manager
from flask_login import UserMixin
from functools import partial
from sqlalchemy import orm, Enum
import enum

db.Model.metadata.reflect(db.engine)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(String(user_id))


class Users(db.Model, UserMixin):
    __table_args__ = {'extend_existing': True}
    userID = db.Column(db.String(15), primary_key=True)
    name = db.Column(db.String(20), nullable = True)
    address = db.Column(db.String(100))
    password = db.Column(db.String(60), nullable=False)
    

    def __repr__(self):
        return "User('{self.username}')"



    

  
