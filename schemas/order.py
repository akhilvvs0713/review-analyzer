from pydantic import BaseModel

class Order(BaseModel):
    item_name: str
    quantity: int