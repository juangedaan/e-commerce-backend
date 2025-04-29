from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.product import ProductOut
from app.services.product_service import list_products, get_product_by_id
from typing import List

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/", response_model=List[ProductOut])
def get_products(db: Session = Depends(get_db)):
    return list_products(db)


@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    return get_product_by_id(product_id, db)

