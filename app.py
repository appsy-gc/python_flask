from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
# Marshmallow library to convert from python objects to JSON - 'Serialisation' & 'Deserialisation'
from flask_marshmallow import Marshmallow

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://overlord:L0neW0lf%($!@localhost:5432/demo_app_db"

# Initialise SQLA and MA after app.config
# Initialise SQLAlcemy
db = SQLAlchemy(app)
# Initialise Marshmallow
ma = Marshmallow(app)

# Create model - DB Table
class Product(db.Model):
    # Define table name
    __tablename__ = "products"
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    # Other items and attributes
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100))
    price = db.Column(db.Float())
    stock = db.Column(db.Integer())

# Marshmallow Schema to tell ma what to focus on for the conversion
class ProductSchema(ma.Schema):
    class Meta:
        # fields for serialisation
        fields = ("id","name", "description", "price", "stock")

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

# Custom CLI Commands
@app.cli.command("create")
def create_tables():
    db.create_all()
    print("Tables created")

@app.cli.command("drop")
def drop_table():
    db.drop_all()
    print("Tables dropped")

@app.cli.command("seed")
def seed_table():
    product0 = Product(
        id = 0,
        name = "Samurai Sword",
        description = "A fine sword for decapitating mofos",
        price = 5000.00,
        stock = 5
    )

    product1 = Product(
        id = 1,
        name = "Rail Gun",
        description = "A devestating weapon",
        price = 1000000.00,
        stock = 1
    )

    product2 = Product(
        id = 2,
        name = "Land mine",
        description = "Hidden fun",
        price = 6969.69,
        stock = 23
    )

    # Add first row with first product
    db.session.add(product0)
    # Add second row with another product
    db.session.add(product1)
    # Add third product
    db.session.add(product2)

    # Commit changes
    db.session.commit()
    print("Table impregnated")

@app.route("/")
def welcome():
    return "Welcome to the products site."

# CRUD Operations
# READ => GET
@app.route("/all_products", methods=["GET"])
def get_products():
    # get all products from the database
    stmt = db.select(Product) # Same as SELECT * FROM PRODUCT which can be extended by adding '.' then where...etc
    products = db.session.scalars(stmt) # scalar for single data, scalars for multiple. Result is in python format
    result = products_schema.dump(products) # 
    return jsonify(result)


# POST


# PUT


# PATCH


# DELETE => DELETE

# Dynamic routing
@app.route("/product/<product>")
def get_product(product):
    return f"<p>You have viewed {product}"

    