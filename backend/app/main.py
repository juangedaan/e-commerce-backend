from fastapi import FastAPI
from app.db.init_db import init_db
from app.api import user, product, purchase

app = FastAPI(
    title="Social Commerce Backend",
    description="Simulated social commerce ecosystem with recommendation engine.",
    version="1.0.0"
)

# Initialize database on app startup (only for development/local)
@app.on_event("startup")
def startup_event():
    init_db()

# Register API routers
app.include_router(user.router)
app.include_router(product.router)
app.include_router(purchase.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Social Commerce Backend!"}

