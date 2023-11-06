from fastapi import FastAPI
from user import router as user_router
from component import router as component_router
from furniture import router as furniture_router
from cart import router as cart_router
from model import router as model_router

app = FastAPI()

app.include_router(user_router, prefix='/user')
app.include_router(component_router, prefix='/component')
app.include_router(furniture_router, prefix='/furniture')
app.include_router(cart_router, prefix='/cart')
app.include_router(model_router, prefix='/model')