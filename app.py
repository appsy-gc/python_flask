from flask import Flask, request
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

class Category(db.Model): # SQLAlchemy
    # Define table name
    __tablename__ = "categories"
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    # Other items and attributes
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100))

# Marshmallow Schema to tell ma what to focus on for the conversion
class ProductSchema(ma.Schema):
    class Meta:
        # fields for serialisation
        fields = ("id","name", "description", "price", "stock")

class CategorySchema(ma.Schema): # Inherit from Schema class in Marshmallow
    class Meta:
        fields = ("id", "name", "description")

# Handle single table
product_schema = ProductSchema()
category_schema = CategorySchema()
# Handle many tables
products_schema = ProductSchema(many=True)
categories_schema = CategorySchema(many=True)

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

    # Create list of categories object
    categories = [
        Category(
            name = "Hand Held"
        ),
        Category(
            name = "Ground Warfare"
        ),
        Category(
            name = "Vehicle Mounted"
        )
    ]
    # Add the list to the session
    db.session.add_all(categories) # .add_all to add the list
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
    result = products_schema.dump(products) # Select the 'many' schema and add serialised schema to products
    # return jsonify(result) < DOESN'T SEEM TO REQUIRE THIS OR MAKE A DIFFERENCE
    return result

# Dynamic Routing for single products
@app.route("/products/<int:product_id>") # Default method = GET
def get_product(product_id): # Use route placeholder as function argument
    stmt = db.select(Product).filter_by(id=product_id)
    product = db.session.scalar(stmt)

    # Exception handling for when product_id does not exist
    if product:
        result = product_schema.dump(product)
        return result
    else:    
        return {"message": f"Product with id: {product_id} does not exist, soz chump"}, 404
        

# (CRUD) CREATE => POST ("/products")
@app.route("/products", methods=["POST"])
def create_product():
    # Import request from flask
    body_data = request.get_json()
    # New instance of Product class and use keys from body_data to assign values
    new_product = Product(
        name = body_data.get("name"),
        description = body_data.get("description"),
        price = body_data.get("price"),
        stock = body_data.get("stock")
    )
    db.session.add(new_product)
    db.session.commit()
    return product_schema.dump(new_product), 201 # 201 Created code returned

# (CRUD) UPDATE => PUT or PATCH ("/products/id")
# PUT replaces an entire product - will create a new product if ID does not exist
# PATCH replaces a value within a product
@app.route("/products/<int:product_id>", methods=["PUT", "PATCH"])
def update_product(product_id):
    stmt = db.select(Product).filter_by(id=product_id)
    product = db.session.scalar(stmt)
    body_data = request.get_json()

    if product:
        # Update and message
        product.name = body_data.get("name") or product.name
        product.description = body_data.get("description") or product.description
        product.price = body_data.get("price") or product.price
        product.stock = body_data.get("stock") or product.stock
        db.session.commit()
        return product_schema.dump(product)
    else:
        # Error message
        return {"message": f"Product with id: {product_id} does not exist, soz chump"}, 404


# (CRUD) DELETE => DELETE ("/products/id")
@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    stmt = db.select(Product).where(Product.id==product_id)
    product = db.session.scalar(stmt)

    if product:
        db.session.delete(product)
        db.session.commit()
        return {"message": f"Product '{product.name}' deleted successfully"}
    else:
        return {"message": f"Product with id: {product_id} does not exist, soz chump"}, 404

# Read all categories > /categories
@app.route("/categories")
def all_categories():
    stmt = db.select(Category) # SELECT * FROM CATEGORIES
    categories = db.session.scalars(stmt) # scalar for single data, scalars for multiple. Result is in python format
    result = categories_schema.dump(categories) # Select the 'many' schema and add serialised schema to categories
    return result
    
# Read single category > /categories/<int:cat_id>
@app.route("/categories/<int:cat_id>")
def get_category(cat_id):
    stmt = db.select(Category).filter_by(id=cat_id) # Select * from categories, where id = cat_id
    category = db.session.scalar(stmt) 

    if category:
        result = category_schema.dump(category) # Convert python object into serialised schema
        return result
    else:
        return {"message": f"Category id {cat_id} does not exist, loser."}, 404

# Create category > /categories [POST]
@app.route("/categories", methods=["POST"])
def create_category():
    body_data = request.get_json()
    new_category = Category(
        name = body_data.get("name"),
        description = body_data.get("description")
    )
    db.session.add(new_category)
    db.session.commit()
    return category_schema.dump(new_category), 201

# Update category > /categories/<int:cat_id [PUT] or [PATCH]


# Delete category > /categories/int:cat_id [DELETE]

