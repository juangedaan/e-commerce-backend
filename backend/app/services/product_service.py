from app.db.models import Product


def list_products(db):
    return db.query(Product).all()
