import csv
import datetime

from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

ENGINE = create_engine("sqlite:///inventory.db", echo=True)
SESSION = sessionmaker(bind=ENGINE)
session = SESSION()
BASE = declarative_base()

class Brand(BASE):
    __tablename__ = "brands"

    brand_id = Column(Integer, primary_key=True)
    brand_name = Column("Brand Name", String, unique=True)

    def __repr__(self):
        return f"Brand ID: {self.brand_id} Brand Name: {self.brand_name}"

class Product(BASE):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True)
    product_name = Column("Product Name", String, unique=True)
    product_quantity = Column("Product Quantity", Integer)
    product_price = Column("Product Price", Float)
    date_updated = Column("Date Updated", Date)
    brand_id = Column(Integer, ForeignKey("brands.brand_id"))

    def __repr__(self):
        return f"Product ID: {self.product_id} Product Name: {self.product_name} Product Quantity: {self.product_quantity} Product Price: {self.product_price}"
    def print(self):
        print(f"Product ID: {self.product_id} Product Name: {self.product_name} Product Quantity: {self.product_quantity} Product Price: {self.product_price}")

def importBrands(session):
    with open("./store-inventory/brands.csv") as csvfile:
        brandsReader = csv.reader(csvfile, delimiter="\n")
        rows = list(brandsReader)
        for row in rows:
            brand = Brand()
            brand.brand_name = row[0]
            session.add(brand)
            try:
                session.commit()
            except IntegrityError as e:
                session.rollback()
                print(e)


def importProducts(session):
    with open("./store-inventory/inventory.csv") as csvfile:
        brandsReader = csv.reader(csvfile, delimiter=",")
        rows = list(brandsReader)
        for row in rows:
            if row[0] == "product_name":
                continue
            product = Product()
            product.product_name = row[0]
            price = row[1].split("$")
            product.product_price = price[1] if len(price) > 1 else price[0]
            product.product_quantity = row[2]
            dateArray = row[3].split("/")
            product.date_updated = datetime.date(
                int(dateArray[2]), int(dateArray[0]), int(dateArray[1]))
            selectedBrand = session.query(Brand).filter(Brand.brand_name == row[4]).first()
            product.brand_id = selectedBrand.brand_id
            session.add(product)
            try:
                session.commit()
            except IntegrityError as e:
                session.rollback()
                print(e)
        