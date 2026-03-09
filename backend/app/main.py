from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(
    title="Social Commerce Backend",
    description="Minimal demo backend with users, products, orders and simple recommendations.",
    version="1.0.0"
)

# in-memory store
users = []
products = []
orders = []

# Data models
class User(BaseModel):
    id: int
    name: str

class Product(BaseModel):
    id: int
    name: str
    price: float

class Order(BaseModel):
    id: int
    user_id: int
    product_ids: List[int]

# root
@app.get("/")
def read_root():
    return {"message": "Welcome to the Social Commerce Backend!"}

# user endpoints
@app.post("/users/", response_model=User)
def create_user(user: User):
    users.append(user)
    return user

@app.get("/users/", response_model=List[User])
def list_users():
    return users

# product endpoints
@app.post("/products/", response_model=Product)
def create_product(product: Product):
    products.append(product)
    return product

@app.get("/products/", response_model=List[Product])
def list_products():
    return products

# order endpoints
@app.post("/orders/", response_model=Order)
def create_order(order: Order):
    if not any(u.id == order.user_id for u in users):
        raise HTTPException(status_code=400, detail="User not found")
    for pid in order.product_ids:
        if not any(p.id == pid for p in products):
            raise HTTPException(status_code=400, detail=f"Product {pid} not found")
    orders.append(order)
    return order

@app.get("/orders/", response_model=List[Order])
def list_orders():
    return orders

# recommendation endpoint
@app.get("/recommendations/{user_id}")
def recommend(user_id: int):
    # simple static recommendation: return first 3 products not ordered by user
    purchased = []
    for o in orders:
        if o.user_id == user_id:
            purchased.extend(o.product_ids)
    recs = [p for p in products if p.id not in purchased][:3]
    return {"user_id": user_id, "recommendations": recs}

