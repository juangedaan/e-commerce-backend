from sqlalchemy.orm import Session
from app.db.models import Product
from typing import List


def list_products(db: Session) -> List[Product]:
    return db.query(Product).all()


def get_product_by_id(product_id: int, db: Session) -> Product | None:
    return db.query(Product).filter(Product.id == product_id).first()

