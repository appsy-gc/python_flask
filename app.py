from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://overlord:L0neW0lf%($!@localhost:5432/demo_app_db"

db = SQLAlchemy(app)

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

    # Alternate way of adding data
    product2 = Product()
    product2.name = "Land mine"
    product2.price = 6969.69
    product2.stock = 23

    # Add first row with first product
    db.session.add(product0)
    # Add second row with another product
    db.session.add(product1)
    # Add third product
    db.session.add(product2)

    # Commit changes
    db.session.commit()
    print("Table impregnated")