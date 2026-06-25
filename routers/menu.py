from fastapi import APIRouter
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from cache import get_cache, set_cache

router = APIRouter()

@router.get("/menu")
def get_menu():
    cached = get_cache("menu_items")
    if cached:
        print("Serving from CACHE")
        return cached

    print("Serving from DATABASE")
    menu = [
        {"id": 1, "name": "Pizza", "price": 199},
        {"id": 2, "name": "Burger", "price": 99},
        {"id": 3, "name": "Pasta", "price": 149}
    ]
    set_cache("menu_items", menu, expire_seconds=60)
    return menu