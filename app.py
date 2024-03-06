from flask import *
from sqlalchemy import select
from pathlib import Path
from db import db
from models import Product, Customer

app = Flask(__name__)
# This will make Flask use a 'sqlite' database with the filename provided
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
# This will make Flask store the database file in the path provided
app.instance_path = Path(".").resolve()
# This helps connect to the database 
db.init_app(app)

@app.route("/")
def home():
    return render_template("base.html")
@app.route("/customers")

def customer_list():
    # statement = db.select(Customer.name).where(Customer.phone == "236-169-6400")
    # records = db.session.execute(statement)
    # customer = records.scalars().all()
    # print(customer)
    statement = select(Customer).order_by(Customer.name)
    records = db.session.execute(statement)
    data = records.scalars().all()
    return render_template("customers.html", customers = data)

@app.route("/products")
def product_list():
    # statement = select(Product.price).where(Product.name == "eggs")
    # records = db.session.execute(statement)
    # data = records.scalars().all()
    # print(data)
    statement = select(Product).order_by(Product.name)
    records = db.session.execute(statement)
    data = records.scalars().all()
    return render_template("products.html", products = data)

# Endpoints API of customers data
@app.route("/api/customers")
def customers_json():
    statement = select(Customer).order_by(Customer.name) 
    results = db.session.execute(statement)
    customers = [] # output variable
    for customer in results.scalars().all(): 

        # json_record = { 
        #     "id": customer.id, 
        #     "name": customer.name, 
        #     "phone": customer.phone, 
        #     "balance": customer.balance
        # }      
        # customers.append(json_record) 

        customers.append(customer.to_json()) 

    return jsonify(customers)

# Endpoints API of customer who has specific customer_id
# @app.route("/api/customers/<int:customer_id>")
# def customer_detail_json(customer_id):
#     statement = select(Customer).where(Customer.id == customer_id) 
#     result = db.session.execute(statement)
#     customers = [] # output variable
#     for customer in result.scalars().all(): 
#         json_record = { 
#             "id": customer.id, 
#             "name": customer.name, 
#             "phone": customer.phone, 
#             "balance": customer.balance
#         }      
#         customers.append(json_record) 
#     return jsonify(customers)

@app.route("/api/customers/<int:customer_id>", methods=["DELETE"])
def customer_delete(customer_id):
    customer = db.session.execute(select(Customer).where(Customer.id == customer_id)) 
    # This will delete a Customer instance from database

    db.session.delete(customer) 
    db.session.commit()
    return "deleted"