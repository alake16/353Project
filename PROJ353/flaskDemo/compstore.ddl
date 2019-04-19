create database compstore

create table users(userID int Primary Key, name varchar(20),
	address varchar(100), password varchar(60))
	
create table products (productID int primary key, productName varchar(100), 
	price int, categoryID int)
	
create table admin (adminID int primary key)

create table orders(orderID int primary key, custID int, totalPrice int)

create table order_line(order_line int primary key, orderID int, quantity int,
	custID int, productID int)
	
create table category(categoryID int primary key, categoryname varchar(100))

alter table products add foreign key (categoryID) refrences category.categoryID

alter table admin add foreign key (adminID) references users.userID

alter table orders add foreign key(custID) references users.userID

alter table order_line add foreign key(orderID) references orders.orderID

alter table order_line add foreign key(custID) references users.userID

alter table order_line add foreign key(productID) references products.productID



