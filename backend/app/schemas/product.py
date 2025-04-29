from pydantic import BaseModel
from typing import Optional

class ProductOut(BaseModel):
    id: int
    title: str
    category: Optional[str] = None
    price: Optional[float] = None
    rating: Optional[float] = None
    reviews_count: Optional[int] = None
    image_url: Optional[str] = None

    class Config:
        orm_mode = True

