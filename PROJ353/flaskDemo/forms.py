from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField, DateField, SelectField, HiddenField, DecimalField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError,Regexp
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flaskDemo import db
from flaskDemo.models import Users, category, products
from wtforms.fields.html5 import DateField

possCategories = category.query.all()
myChoices = [(row.categoryID, row.categoryname) for row in possCategories]

possCPU = db.session.query(products).filter_by(categoryID = 1)
#for row in possCPU:
#    if row.categoryID == 1
#        cpuList.append(row)
cpuChoices = [(row.productID, row.productName) for row in possCPU]


possMem = db.session.query(products).filter_by(categoryID = 2)
memChoices = [(row.productID, row.productName) for row in possMem]

possStorage = db.session.query(products).filter_by(categoryID = 3)
storageChoices = [(row.productID, row.productName) for row in possStorage]

possPower  = db.session.query(products).filter_by(categoryID = 4)
powerChoices = [(row.productID, row.productName) for row in possPower]

possGPU = db.session.query(products).filter_by(categoryID = 5)
gpuChoices = [(row.productID, row.productName) for row in possGPU]

possFans = db.session.query(products).filter_by(categoryID = 6)
fanChoices = [(row.productID, row.productName) for row in possFans]

possMother = db.session.query(products).filter_by(categoryID = 7)
motherBoardChoices = [(row.productID, row.productName) for row in possMother]

products = products.query.all()
productsChoices = [(row.productID, row.productName) for row in products]

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    address= StringField('address',
                        validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = Users.query.filter_by(name=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

class editProductForm(FlaskForm):
    price = IntegerField('NEW PRICE')
    submit = SubmitField('CHANGE PRICE')


class customBuildForm(FlaskForm):
    CPU = SelectField('CPU', choices = cpuChoices, coerce = int)
    Memory = SelectField('Memory', choices = memChoices, coerce =int)
    Storage = SelectField('Storage', choices = storageChoices, coerce = int)
    power = SelectField('Power Supply', choices = powerChoices, coerce = int)
    gpu = SelectField('GPU', choices = gpuChoices, coerce = int)
    fan = SelectField('Fan', choices = fanChoices, coerce = int)
    mother = SelectField('MotherBoard', choices = motherBoardChoices, coerce = int)
    submit = SubmitField('Submit')


class guestCheckoutForm(FlaskForm):
    name = StringField('Name')
    address = StringField('Address')
    password = StringField('password')
    submit = SubmitField('Place order')

class addNewForm(FlaskForm):
    productName = StringField('Product Name')
    productPrice = DecimalField('Product Price')
    categoryID = SelectField('Category', choices = myChoices, coerce = int)
    submit = SubmitField('Add')

class addCompatibilityRestrictionForm(FlaskForm):
    productAName = SelectField('Product A', choices = productsChoices, coerce = int)
    productBName = SelectField('Product B', choices = productsChoices, coerce = int)
    submit = SubmitField('Add')


class LoginForm(FlaskForm):
    username = StringField('username',
                        validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    name = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    address = StringField('Address',
                        validators=[DataRequired(), Length(min=2, max=40)])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

