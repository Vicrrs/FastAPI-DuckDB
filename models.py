from pydantic import BaseModel

class Item(BaseModel):
    id: int
    name: str
    description: str
    price: float
    in_stock: bool

