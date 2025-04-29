from pydantic import BaseModel
from datetime import datetime

class PurchaseCreate(BaseModel):
    user_id: int
    product_id: int
    quantity: int = 1

class PurchaseOut(BaseModel):
    id: int
    user_id: int
    product_id: int
    quantity: int
    purchased_at: datetime

    class Config:
        orm_mode = True

