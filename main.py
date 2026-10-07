from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from models import Product
from database import session, engine
import database_models
from sqlalchemy.orm import Session

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"]
)

database_models.Base.metadata.create_all(bind=engine)


@app.get("/")
def greet():
    return 'welcome to udaya learn'


products = [
    Product(id=1, name="phone", description="budget11", price=99, quantity=10),
    Product(id=2, name="tablet", description="budget123", price=66, quantity=9),
    Product(id=3, name="pc", description="budget33", price=78, quantity=7),
    Product(id=4, name="computer", description="budget44", price=35, quantity=1),
]


def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


def init_db():
    db = session()
    count = db.query(database_models.Product).count
    if count == 0:
        for product in products:
            db.add(database_models.Product(**product.model_dump()))
        db.commit()


init_db()


@app.get("/products")
def get_all_products(db: Session = Depends(get_db)):
    db_products = db.query(database_models.Product).all()
    return db_products


@app.get("/products/{id}")
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(
        database_models.Product.id == id).first()
    if db_product:
        return db_product
    else:
        return "product not found"


@app.post("/products")
def add_product(product: Product, db: Session = Depends(get_db)):
    db.add(database_models.Product(**product.model_dump()))
    db.commit()
    return product


@app.put("/products/{id}")
def update_product(id: int, product: Product, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(
        database_models.Product.id == id).first()
    if db_product:
        db_product.name = database_models.Product(**product.model_dump()).name
        db_product.description = database_models.Product(
            **product.model_dump()).description
        db_product.price = database_models.Product(
            **product.model_dump()).price
        db_product.quantity = database_models.Product(
            **product.model_dump()).quantity
        db.commit()
        return "product updated"
    else:
        return "product not found"


@app.delete("/products/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(
        database_models.Product.id == id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return "deleted"
    else:
        return "product not found"
