from fastapi import APIRouter, HTTPException
import json
from pydantic import BaseModel
from user import User

class authenticatedUser(BaseModel):
    username: str
    password: str

router = APIRouter()

authData = 'data/auth.json'

with open(authData, 'r') as read_file:
    data = json.load(read_file)

authenticatedUser = []

@router.post('/login')
async def login(authenticatedUser: authenticatedUser):
    if (authenticatedUser == []):
        flagUsernameExists = False

        for 