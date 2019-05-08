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
        return f"User('{self.name}', '{self.address}')"


class Admin(db.Model):
    __table_args__ = {'extend_existing': True}
    adminID = db.Column(db.Integer, primary_key=True)
    def get_id(self):
        return (self.adminID)
    def __repr__(self):
        return f"User('{self.adminID}')"

class employees(db.Model):
    __table_args__ = {'extend_existing': True}
    EID = db.Column(db.Integer, primary_key=True)
    DID = db.Column(db.Integer)
    payrate = db.Column(db.DECIMAL)
    def get_id(self):
        return (self.EID)
    def __repr__(self):
        return f"Employee('{self.EID}', '{self.DID}', '{self.payrate}')"

class payroll(db.Model):
    __table_args__ = {'extend_existing' : True}
    PRID = db.Column(db.Integer, primary_key = True)
    EID = db.Column(db.Integer)
    hours = db.Column(db.DECIMAL)
    SD = db.Column(db.DateTime)
    ED = db.Column(db.DateTime)
    def get_id(self):
        return (self.PRID)
    def __repr__(self):
        return f"payroll( '{self.EID}', '{self.hours}', '{self.SD}', '{self.ED}')"

class category(db.Model):
    __table_args__ = {'extend_existing': True}
    categoryID = db.Column(db.Integer, primary_key=True)
    categoryName = db.Column(db.String(100))
    def get_id(self):
        return (self.categoryID)
    def __repr__(self):
        return f"User('{self.categoryID}')"

class orders(db.Model):
    __table_args__ = {'extend_existing': True}
    custID = db.Column(db.Integer)
    orderid = db.Column(db.Integer, primary_key = True)
    totalPrice = db.Column(db.Integer)
    def get_id(self):
        return (self.orderid)
    def __repr__(self):
        return f"User('{self.orderid}')"

class order_line(db.Model):
    __table_args__ = {'extend_existing' : True}
    order_line = db.Column(db.Integer, primary_key = True)
    custID = db.Column(db.Integer)
    orderID = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    productID = db.Column(db.Integer)
    def get_id(self):
        return (self.order_line)
    def __repr__(self):
        return f"order_line('{self.order_line}', '{self.orderID}', '{self.custID}', '{self.productID}' )"


class products(db.Model):
    __table_args__ = {'extend_existing': True}
    productID = db.Column(db.Integer, primary_key=True)
    productName = db.Column(db.String(100), nullable=False)
    productPrice = db.Column(db.DECIMAL(10,2))
    categoryID = db.Column(db.Integer)
    def get_id(self):
        return (self.productID)
        
    def __repr__(self):
        return f"products('{self.productID}','{self.productName}', '{self.productPrice}')"

class orderstofufill(db.Model):
    __table_args__ = {'extend_existing': True}
    PK = db.Column(db.Integer, primary_key=True)
    OID = db.Column(db.Integer)
    def get_id(self):
        return (self.PK)
    
    def __repr__(self):
        return f"ordersToFufill('{self.OID}', '{self.PK}')"

class sales(db.Model):
    __table_args__ = {'extend_existing': True}
    SID = db.Column(db.Integer, primary_key = True )
    PID = db.Column(db.Integer)
    TS = db.Column(db.DECIMAL)
    def get_id(self):
        return (self.PK)
    
    def __repr__(self):
        return f"sales('{self.PID}', '{self.TS}')"


class compatibility_restriction(db.Model):
    __table_args__ = {'extend_existing' : True}
    productAID = db.Column(db.Integer, primary_key = True)
    productBID = db.Column(db.Integer, primary_key = True)
    def get_id(self):
        return (self.productAID, self.productBID)
    def __repr__(self):
        return f"User('{self.productAID, self.productBID}')"


  
