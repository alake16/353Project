import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskDemo import app, db, bcrypt
from flaskDemo.forms import RegistrationForm, LoginForm, UpdateAccountForm, addNewForm
from flaskDemo.models import Users, products, Admin
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime



@app.route("/home")
def home():
    Admins = db.session.query(Admin.adminID)
    for row in Admins:
        print (row[0])
    return render_template('home.html', title='home')


@app.route("/products", methods=['GET','POST'])
@login_required
def displayProducts():
    productsList = db.session.query(products.productName, products.productID).all()
    displayProduct = list()
    for row in productsList:
        print (row)
    return render_template('products.html', products = productsList, title = 'products')


@app.route("/product/<productID>", methods = ['GET', 'POST'])
@login_required
def indiProduct(productID):
    indiProd = products.query.get(productID)
    price = indiProd.price
    return render_template('indiProd.html', title = 'indiProd', productName = indiProd.productName, price = price)

@app.route("/adminPage", methods = ['Get', 'POST'])
@login_required
def adminPage():
    form = addNewForm()
    if form.validate_on_submit():
        prod = products(productID = form.productID.data, productName = form.productName.data, price = form.productPrice.data, categoryID = form.categoryID.data)
        db.session.add(prod)
        db.session.commit()
        flash('product added', 'sucess')
    return render_template('admin.html', title = 'ADMIN', form =form)



@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = Users(name=form.username.data, address=form.address.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('home', userID = user.userID))
    return render_template('register.html', title='Register', form=form)

@app.route("/")
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(name=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('login successful', 'success')
            Admins = db.session.query(Admin.adminID)
            for row in Admins:
                if row.adminID == user.userID:
                    return redirect(url_for('adminPage'))
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


@app.route("/dept/new", methods=['GET', 'POST'])
@login_required
def new_dept():
    form = DeptForm()
    if form.validate_on_submit():
        dept = Department(dname=form.dname.data, dnumber=form.dnumber.data,mgr_ssn=form.mgr_ssn.data,mgr_start=form.mgr_start.data)
        db.session.add(dept)
        db.session.commit()
        flash('You have added a new department!', 'success')
        return redirect(url_for('home'))
    return render_template('create_dept.html', title='New Department',
                           form=form, legend='New Department')



@app.route("/add", methods=['GET', 'POST'])
@login_required
def add():
    print('ADDDD')
    form = addForm()
    print('add2')
    if form.validate_on_submit():
        flash('validated', 'success')
        ssnnumber = form.essn.data
        return redirect(url_for('add2', ssn = ssnnumber))
    return render_template('add.html', title='New add',
                           form=form, legend='New add')



@app.route("/add2/<ssn>", methods=['GET', 'POST'])
@login_required
def add2(ssn):
    form = add2Form()
    if form.validate_on_submit():
        pnum = form.pno.data
        print(pnum)
        print(ssn)
        WO = Works_On(essn=ssn, pno=form.pno.data, hours=form.hours.data)
        check = Works_On.query.get([ssn,pnum])
        if check:
            flash('item already in database try again', 'success')
            return redirect(url_for('add'))
        db.session.add(WO)
        db.session.commit()
        flash('You have added a new WO!', 'success')
        return redirect(url_for('join'))

    return render_template('add2.html', title='New add2',
                           form=form, legend='New add2')




@app.route("/dept/<dnumber>")
@login_required
def dept(dnumber):
    dept = Department.query.get_or_404(dnumber)
    return render_template('dept.html', title=dept.dname, dept=dept, now=datetime.utcnow())

@app.route("/employee/<ssn>/proj/<pno>")
@login_required
def empl(ssn,pno):
    empl = Employee.query.get_or_404(ssn)
    proj = Project.query.get_or_404(pno)
    return render_template('empl.html', title=Employee.lname, empl=empl, proj = proj, now=datetime.utcnow())


@app.route("/dept/<dnumber>/update", methods=['GET', 'POST'])
@login_required
def update_dept(dnumber):
    dept = Department.query.get_or_404(dnumber)
    currentDept = dept.dname

    form = DeptUpdateForm()
    if form.validate_on_submit():          # notice we are are not passing the dnumber from the form
        if currentDept !=form.dname.data:
            dept.dname=form.dname.data
        dept.mgr_ssn=form.mgr_ssn.data
        dept.mgr_start=form.mgr_start.data
        db.session.commit()
        flash('Your department has been updated!', 'success')
        return redirect(url_for('dept', dnumber=dnumber))
    elif request.method == 'GET':             
        form.dnumber.data = dept.dnumber   # notice that we ARE passing the dnumber to the form
        form.dname.data = dept.dname
        form.mgr_ssn.data = dept.mgr_ssn
        form.mgr_start.data = dept.mgr_start
    return render_template('update_dept.html', title='Update Department',
                           form=form, legend='Update Department')          # note the update template!


@app.route("/empl/update/", methods=['GET', 'POST'])
@login_required
def update_empl(ssn, pno):
    
    form = EmplUpdateForm()
    
    if form.validate_on_submit():
        empl = Works_On(essn=form.essn.data, pno=form.pno.data, hours=form.hours.data)
        db.session.add(empl)
        db.session.commit()
        flash('Your WORKS ON has been updated!', 'success')
        return redirect(url_for('join'))
    return render_template('update_empl.html', title='Update EMPL',
                           form=form, legend='Update EMPL')


@app.route("/dept/<dnumber>/delete", methods=['POST'])
@login_required
def delete_dept(dnumber):
    dept = Department.query.get_or_404(dnumber)
    db.session.delete(dept)
    db.session.commit()
    flash('The department has been deleted!', 'success')
    return redirect(url_for('home'))

@app.route("/empl/<ssn>/delete/<pno>", methods=['POST'])
@login_required
def delete_empl(ssn, pno):
    empl = Works_On.query.get_or_404([ssn, pno])
    db.session.delete(empl)
    db.session.commit()
    flash('The Employee has been deleted!', 'success')
    return redirect(url_for('home'))
