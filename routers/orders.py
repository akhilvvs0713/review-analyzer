from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import get_db
from models import Order as OrderModel
from schemas.order import Order
from auth import get_current_user
router = APIRouter()

@router.post("/order")
def place_order(order: Order, db: Session = Depends(get_db)):
    new_order = OrderModel(
        item_name=order.item_name,
        quantity=order.quantity
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return {"id": new_order.id, "message": f"Order placed for {order.item_name}"}

@router.get("/orders")
def get_orders(db: Session = Depends(get_db)):
    orders = db.query(OrderModel).all()
    return orders
from auth import get_current_user

@router.post("/order")
def place_order(
    order: Order,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)  # ← protected
):
    new_order = OrderModel(
        item_name=order.item_name,
        quantity=order.quantity
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return {
        "id": new_order.id,
        "message": f"Order placed by {current_user['email']}"
    }