import pandas as pd
import psycopg2
from psycopg2.extras import execute_batch
import os

# Load environment variables or hardcode your DB credentials here
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'socialdb')
DB_USER = os.getenv('DB_USER', 'yourusername')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'yourpassword')

CSV_FILE_PATH = 'assets/amazon-products.csv'  # Update path if needed

def create_products_table(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id SERIAL PRIMARY KEY,
            title TEXT,
            category TEXT,
            price FLOAT,
            rating FLOAT,
            reviews_count INT,
            image_url TEXT
        );
    """)

def load_products_from_csv(cursor, file_path):
    df = pd.read_csv(file_path)

    # Normalize/adjust columns
    df = df.rename(columns={
        'title': 'title',
        'category': 'category',
        'price': 'price',
        'rating': 'rating',
        'reviews': 'reviews_count',
        'imgUrl': 'image_url'
    })

    # Select only the fields we care about
    columns = ['title', 'category', 'price', 'rating', 'reviews_count', 'image_url']
    df = df[columns]

    # Replace NaN with None
    df = df.where(pd.notnull(df), None)

    records = df.to_records(index=False)
    execute_batch(cursor,
        """
        INSERT INTO products (title, category, price, rating, reviews_count, image_url)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT DO NOTHING;
        """,
        records
    )

def main():
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    conn.autocommit = True
    cursor = conn.cursor()

    create_products_table(cursor)
    load_products_from_csv(cursor, CSV_FILE_PATH)

    cursor.close()
    conn.close()
    print("✅ Products loaded successfully!")

if __name__ == "__main__":
    main()

