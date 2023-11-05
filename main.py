from fastapi import FastAPI
from user import router as user_router
from component import router as component_router
from furniture import router as furniture_router

app = FastAPI()

app.include_router(user_router, prefix='/user')
app.include_router(component_router, prefix='/component')
app.include_router(furniture_router, prefix='/furniture')
