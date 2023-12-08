from fastapi import FastAPI
from user import router as user_router
from component import router as component_router
from furniture import router as furniture_router
from cart import router as cart_router
from model import router as model_router
from auth import router as auth_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router, prefix='/user')
app.include_router(component_router, prefix='/component')
app.include_router(furniture_router, prefix='/furniture')
app.include_router(cart_router, prefix='/cart')
app.include_router(model_router, prefix='/model')
app.include_router(auth_router, prefix='/token')

@app.get('/')
async def welcome():
    return {"message": "Hello there!"}
