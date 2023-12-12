# TechDegree-Unit4
Project Overview

Use your knowledge of CSV, file reading and creation, and SQLAlchemy to build a console application that allows you to easily interact with inventory data. You will first need to read in the data, clean it, and add it to a SQLite database. Your database will have two tables, one for each CSV file. Next, you will create a console application using SQLAlchemy’s ORM methods to give users the ability to view records, create records, edit and delete records, and display some analysis of the data. The users may also have the ability to create a backup of the data where two new CSV files are created reflecting the current state of the database.

# Initial Solution Design
* import db
* design menu ui
* design controller
* Flesh it all out

# classes
Classes in this project are also models.

## Brand
* brand_id(primary key)
* brand_name

## Product 
* product_id(primary key)
* Product Name
* Product Quantity
* Product Price
* Date Updated
* brand_id (foreign key)
