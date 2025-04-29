from app.db.session import engine, get_db
from app.db.models import Base, Product
from sqlalchemy.orm import Session
import pandas as pd
import os

def init_db():
    # Create tables
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created successfully.")

    # Load products if database is empty
    db: Session = next(get_db())
    product_count = db.query(Product).count()

    if product_count == 0:
        print("ℹ️ No products found in database. Loading sample products...")
        load_products(db)
    else:
        print(f"ℹ️ Database already has {product_count} products. Skipping load.")

def load_products(db: Session):
    # Adjust the path if running from a different context
    csv_path = os.path.join(os.path.dirname(__file__), "../../assets/amazon-products.csv")

    if not os.path.exists(csv_path):
        print(f"❌ CSV file not found: {csv_path}")
        return

    df = pd.read_csv(csv_path)

    # Normalize/adjust columns
    df = df.rename(columns={
        'title': 'title',
        'category': 'category',
        'price': 'price',
        'rating': 'rating',
        'reviews': 'reviews_count',
        'imgUrl': 'image_url'
    })

    columns = ['title', 'category', 'price', 'rating', 'reviews_count', 'image_url']
    df = df[columns]
    df = df.where(pd.notnull(df), None)

    products = [
        Product(
            title=row['title'],
            category=row['category'],
            price=row['price'],
            rating=row['rating'],
            reviews_count=row['reviews_count'],
            image_url=row['image_url']
        )
        for _, row in df.iterrows()
    ]

    db.bulk_save_objects(products)
    db.commit()
    print(f"✅ {len(products)} products loaded into database.")

if __name__ == "__main__":
    init_db()

