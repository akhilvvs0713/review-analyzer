import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from fastapi import FastAPI
from database import engine, Base
from routers import menu, orders, users

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Food Delivery API")

app.include_router(menu.router, prefix="/v1", tags=["Menu"])
app.include_router(orders.router, prefix="/v1", tags=["Orders"])
app.include_router(users.router, prefix="/v1", tags=["Users"])
from fastapi import FastAPI
from database import engine, Base
from routers import menu, orders, users
from routers import auth as auth_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Food Delivery API")

app.include_router(auth_router.router, prefix="/v1", tags=["Auth"])
app.include_router(menu.router, prefix="/v1", tags=["Menu"])
app.include_router(orders.router, prefix="/v1", tags=["Orders"])
app.include_router(users.router, prefix="/v1", tags=["Users"])

from routers import menu, orders, users, files
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

app.include_router(files.router, prefix="/v1", tags=["Files"])

from routers import chat

app.include_router(chat.router, prefix="/v1", tags=["Chat"])
from routers import analyze
app.include_router(analyze.router, prefix="/v1", tags=["Analysis"])