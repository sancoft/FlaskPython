from db import db
import csv
from models import Product, Customer
from app import app

def getData(path, dbType):
    with open(path, "r") as file:
        data = csv.DictReader(file)
        for each in data:
            if dbType == "ctm":
                obj = Customer(name=each["name"], phone=each["phone"])
            elif dbType == "pdt":
                obj = Product(name=each["name"], price=each["price"])
            db.session.add(obj)
        db.session.commit()

def initData():
    with app.app_context(): 
        db.drop_all()
        db.create_all()
        getData("./data/customers.csv", "ctm")
        getData("./data/products.csv", "pdt")

if __name__ == "__main__": 
    initData()
    app.run(debug=True, port=8888)