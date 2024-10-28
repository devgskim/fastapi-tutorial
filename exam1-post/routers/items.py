from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class Item(BaseModel):
    name: str
    price: float

@router.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@router.post("/items/")
def create_item(item: Item):
    return {"item_name": item.name, "item_price": item.price}

