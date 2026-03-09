from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
import time
import hashlib

app = FastAPI(
    title="Social Commerce Backend",
    description="Comprehensive demo backend with users, products, orders, carts, reviews, and advanced recommendations.",
    version="2.0.0"
)

# in-memory store
users = []
products = []
orders = []
carts = []
reviews = []
sessions = {}

# Data models
class User(BaseModel):
    id: int
    name: str
    email: str

class Product(BaseModel):
    id: int
    name: str
    price: float
    category: str
    description: Optional[str] = None

class Order(BaseModel):
    id: int
    user_id: int
    product_ids: List[int]
    total: float
    status: str = "pending"

class CartItem(BaseModel):
    product_id: int
    quantity: int

class Cart(BaseModel):
    user_id: int
    items: List[CartItem] = []

class Review(BaseModel):
    id: int
    user_id: int
    product_id: int
    rating: int
    comment: Optional[str] = None

class LoginRequest(BaseModel):
    email: str
    password: str

# Authentication simulation
def authenticate(token: str):
    if token not in sessions or sessions[token] < time.time():
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return sessions[token]

@app.post("/login")
def login(request: LoginRequest):
    # Simple hash simulation
    token = hashlib.md5(f"{request.email}:{request.password}".encode()).hexdigest()
    sessions[token] = time.time() + 3600  # 1 hour
    return {"token": token}

# root
@app.get("/")
def read_root():
    return {"message": "Welcome to the Social Commerce Backend!"}

# user endpoints
@app.post("/users/", response_model=User)
def create_user(user: User):
    if any(u.email == user.email for u in users):
        raise HTTPException(status_code=400, detail="Email already exists")
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
def list_products(category: Optional[str] = None):
    if category:
        return [p for p in products if p.category == category]
    return products

@app.get("/products/{product_id}", response_model=Product)
def get_product(product_id: int):
    for p in products:
        if p.id == product_id:
            return p
    raise HTTPException(status_code=404, detail="Product not found")

# cart endpoints
@app.post("/cart/", response_model=Cart)
def add_to_cart(cart: Cart):
    existing = next((c for c in carts if c.user_id == cart.user_id), None)
    if existing:
        existing.items.extend(cart.items)
    else:
        carts.append(cart)
    return cart

@app.get("/cart/{user_id}", response_model=Cart)
def get_cart(user_id: int):
    cart = next((c for c in carts if c.user_id == user_id), Cart(user_id=user_id))
    return cart

# review endpoints
@app.post("/reviews/", response_model=Review)
def create_review(review: Review):
    reviews.append(review)
    return review

@app.get("/reviews/{product_id}", response_model=List[Review])
def get_reviews(product_id: int):
    return [r for r in reviews if r.product_id == product_id]

# order endpoints
@app.post("/orders/", response_model=Order)
def create_order(order: Order):
    if not any(u.id == order.user_id for u in users):
        raise HTTPException(status_code=400, detail="User not found")
    for pid in order.product_ids:
        if not any(p.id == pid for p in products):
            raise HTTPException(status_code=400, detail=f"Product {pid} not found")
    order.total = sum(p.price for p in products if p.id in order.product_ids)
    orders.append(order)
    return order

@app.get("/orders/", response_model=List[Order])
def list_orders():
    return orders

# advanced recommendation endpoint
@app.get("/recommendations/{user_id}")
def recommend(user_id: int):
    # Collaborative filtering simulation: recommend based on similar users' purchases
    user_orders = [o for o in orders if o.user_id == user_id]
    purchased = set()
    for o in user_orders:
        purchased.update(o.product_ids)

    # Find similar users (users who bought similar products)
    similar_users = set()
    for o in orders:
        if o.user_id != user_id and any(pid in purchased for pid in o.product_ids):
            similar_users.add(o.user_id)

    # Recommend products bought by similar users but not by this user
    rec_ids = set()
    for o in orders:
        if o.user_id in similar_users:
            rec_ids.update(o.product_ids)
    rec_ids -= purchased

    # Also include popular products and reviews
    product_scores = {}
    for r in reviews:
        if r.product_id not in product_scores:
            product_scores[r.product_id] = 0
        product_scores[r.product_id] += r.rating

    # Sort by score and take top 5
    sorted_recs = sorted(rec_ids, key=lambda pid: product_scores.get(pid, 0), reverse=True)[:5]
    recs = [p for p in products if p.id in sorted_recs]
    return {"user_id": user_id, "recommendations": recs}

