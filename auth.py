from fastapi import APIRouter, HTTPException, Depends, status
import json
import jwt
from pydantic import BaseModel
from passlib.hash import bcrypt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from user import auth_user

router = APIRouter()

JWT_Secret = 'randomjwtseed'
JWT_Algorithm = 'HS256'     

@router.post('/')
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = auth_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    payload = {"sub": form_data.username}
    token = jwt.encode(payload, JWT_Secret, algorithm=JWT_Algorithm)

    return {"access_token": token, "token_type": "bearer"}
