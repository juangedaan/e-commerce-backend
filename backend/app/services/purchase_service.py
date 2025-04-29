from sqlalchemy.orm import Session
from app.db.models import Purchase
from app.schemas.purchase import PurchaseCreate


def create_purchase(data: PurchaseCreate, db: Session) -> Purchase:
    purchase = Purchase(
        user_id=data.user_id,
        product_id=data.product_id,
        quantity=data.quantity,
    )
    db.add(purchase)
    db.commit()
    db.refresh(purchase)
    return purchase


def list_purchases_by_user(user_id: int, db: Session):
    return db.query(Purchase).filter(Purchase.user_id == user_id).all()

