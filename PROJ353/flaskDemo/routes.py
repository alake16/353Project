import os
import mysql.connector
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskDemo import app, db, bcrypt
from flaskDemo.forms import RegistrationForm, LoginForm, UpdateAccountForm, addNewForm, guestCheckoutForm, customBuildForm, editProductForm
from flaskDemo.models import Users, products, Admin, orders, order_line, category
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime
from sqlalchemy import func

cartList = list()


@app.route("/home")
def home():
    Admins = db.session.query(Admin.adminID)
    for row in Admins:
        print (row[0])
    
    try:
        conn=mysql.connector.connect(host='45.55.59.121',database='compstore',user='compstore',password='453compstore')
        if conn.is_connected():
            print('Connected to MySQL database')
            cursor = conn.cursor()
            cursor.execute("SELECT users.name, users.address, admin.adminID FROM users inner join admin on users.userID = admin.adminID where userID in (select adminID from admin)")
            row = cursor.fetchall()
            print(row)
            cursor = conn.cursor()
            cursor.execute("select count(userID) from users")
            count = cursor.fetchone()
            print(count[0])
    finally:
        conn.close()
    
    return render_template('home.html', title='home', user = row, count = count[0])


@app.route("/order/<total>", methods = ['GET','POST'])
def order(total):
    user = Users.query.get(current_user.get_id())
    newOrder = orders(custID = user.userID, totalPrice = total)
    db.session.add(newOrder)
    db.session.commit()
    return redirect(url_for('orderLine'))

@app.route("/orderLine", methods = ['GET', 'POST'])
def orderLine():
    user = Users.query.get(current_user.get_id())
    orderNumber = db.session.query(func.max(orders.orderID)).scalar()
    for row in cartList:
        newOrderLine = order_line( orderID = orderNumber,custID = user.userID, quantity = 1, productID = row.productID)
        db.session.add(newOrderLine)
        db.session.commit()
    return redirect(url_for('home'))

@app.route("/customBuild", methods = ['GET', 'POST'])
def customBuild():
    form = customBuildForm()
    if form.validate_on_submit():
        cpu = products.query.get(form.CPU.data)
        cartList.append(cpu)
        
        mem = products.query.get(form.Memory.data)
        cartList.append(mem)

        stor = products.query.get(form.Storage.data)
        cartList.append(stor)

        power = products.query.get(form.power.data)
        cartList.append(power)

        gpu = products.query.get(form.gpu.data)
        cartList.append(gpu)

        fan = products.query.get(form.fan.data)
        cartList.append(fan)
        
        mother = products.query.get(form.mother.data)
        cartList.append(mother)
        return redirect(url_for('cart'))
    
    return render_template('customBuild.html', form = form)



@app.route("/userCheckout/<total>", methods = ['GET', 'POST'])
def userCheckout(total):
    user = Users.query.get(current_user.get_id())
    return render_template('userCheckOut.html', user = user, total = total)

@app.route("/guestCheckout/<total>", methods = ['GET', 'POST'])
def guestCheckout(total):
    form = guestCheckoutForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = Users(name=form.name.data, address=form.address.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        
        return redirect(url_for('home'))
    return render_template('guestCheckOut.html', form = form, total = total )



@app.route("/products", methods=['GET','POST'])
def displayProducts():
    productsList = db.session.query(products.productName, products.productID).all()
    displayProduct = list()
    for row in productsList:
        print (row)
    return render_template('products.html', products = productsList, title = 'products')


@app.route("/product/<productID>", methods = ['GET', 'POST'])
def indiProduct(productID):
    indiProd = products.query.get(productID)
    myList = products.query.join(category, products.categoryID==category.categoryID).add_columns(products.productID, category.categoryname).filter(products.productID == productID)
    
    name = myList[0].categoryname
#    prod = myList['1']
#    mycategory = prod[categoryname]

    
    return render_template('indiProd.html', title = 'indiProd',product = indiProd, categoryName = name)

@app.route("/editProduct/<productID>", methods = ['GET', 'POST'])
def editProduct(productID):
    indiProd = products.query.get(productID)
    form = editProductForm()
    if form.validate_on_submit():
        indiProd.productPrice = form.price.data
        db.session.commit()
        return redirect(url_for('deletePage'))
    return render_template('editProd.html', title = 'editProd',product = indiProd, form=form)

@app.route("/removeProd/<productID>", methods = ['GET', 'POST'])
def removeProd(productID):
    prod = products.query.get(productID)
    db.session.delete(prod)
    db.session.commit()
    flash('product deleted', 'success')
    return redirect(url_for('deletePage'))

@app.route("/cart/<addItem>", methods = ['GET', 'POST'])
def addCart(addItem):
    price = 0
    prod = products.query.get(addItem)
    cartList.append(prod)
    for row in cartList:
        price += row.productPrice
    return render_template('cart.html', cart = cartList, title = 'Cart', total = price)

@app.route("/cart", methods = ['GET', 'POST'])
def cart():
    price = 0
    for row in cartList:
        price += row.productPrice
    return render_template('cart.html', cart = cartList, title = 'Cart', total = price)

@app.route("/displayCategory/<category>", methods = ['GET', 'POST'])
def displayCategory(category):
    prods = db.session.query(products).filter(products.categoryID.in_((category))).all()
    print (prods)
    return render_template('displayCategory.html', products = prods, title = products)

@app.route("/adminPage", methods = ['Get', 'POST'])
@login_required
def adminPage():
    possCategories = category.query.all()
    myChoices = [(row.categoryID, row.categoryname) for row in possCategories]
    
    possMem = db.session.query(products).filter_by(categoryID = 2)
    memChoices = [(row.productID, row.productName) for row in possMem]
    form = addNewForm()
    if form.validate_on_submit():
        prod = products(productName = form.productName.data, productPrice = form.productPrice.data, categoryID = form.categoryID.data)
        db.session.add(prod)
        db.session.commit()
        flash('product added', 'sucess')
        return redirect(url_for('adminPage'))
    return render_template('admin.html', title = 'ADMIN', form =form)

@app.route("/delete", methods = ['Get', 'POST'])
@login_required
def deletePage():
    prods = products.query.all()
    return render_template('delete.html', title = 'DELETE', prods = prods)



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
                    flash(current_user.get_id(), 'success')
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


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.address = form.address.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.address.data = current_user.address
    return render_template('account.html', title='Account', form=form)


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
