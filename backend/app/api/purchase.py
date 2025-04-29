from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.purchase import PurchaseCreate, PurchaseOut
from app.services.purchase_service import create_purchase, list_purchases_by_user
from typing import List

router = APIRouter(prefix="/purchases", tags=["Purchases"])


@router.post("/", response_model=PurchaseOut)
def make_purchase(data: PurchaseCreate, db: Session = Depends(get_db)):
    return create_purchase(data, db)


@router.get("/user/{user_id}", response_model=List[PurchaseOut])
def get_user_purchases(user_id: int, db: Session = Depends(get_db)):
    return list_purchases_by_user(user_id, db)

