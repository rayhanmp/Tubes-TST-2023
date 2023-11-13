from fastapi import APIRouter, HTTPException, Depends, status
import json
import jwt
from pydantic import BaseModel
from passlib.hash import bcrypt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

class User(BaseModel):
  username: str
  password: str
  fullname: str
  address: str

class UserStored(BaseModel):
	id: int
	username: str
	password_hashed: str
	fullname: str
	address: str

router = APIRouter()

JWT_Secret = 'randomjwtseed'
JWT_Algorithm = 'HS256'

# Establish userData dir
userData = 'data/user.json'

with open(userData, 'r') as read_file:
  data = json.load(read_file)

def auth_user(username: str, password_hashed: str):
	for item in data['user']:
		if item['username'] == username:
			if bcrypt.verify(password_hashed, item['password_hashed']):
				return item
	return None

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')
async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, JWT_Secret, algorithms=[JWT_Algorithm])
        username = payload.get('sub')
        for user in data['user']:
            if user['username'] == username:
                return user
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

@router.get('/')
async def read_all_user():
	return data['user']

@router.get('/me')
async def get_user(user: UserStored = Depends(get_current_user)):
	return user

@router.get('/{id}')
async def read_user(id: int):
  for user_item in data['user']:
    if user_item['id'] == id:
      return user_item
  raise HTTPException(
    status_code=404, detail=f'User not found'
  )

@router.post('/')
async def add_user(item: User):
	item_dict = item.dict()

	id = len(data['user']) + 1
	password_hashed = bcrypt.hash(item_dict['password'])

	item_found = False
	for user_item in data['user']:
		if user_item['username'] == item_dict['username']:
			item_found = True
			return user_item['username'] + " is already taken. Please try other username."
	
	if not item_found:
		newUser = {"id": id, "username": item_dict['username'], "password_hashed": password_hashed, "fullname": item_dict['fullname'], "address": item_dict['address']}
		data['user'].append(newUser)
		with open(userData,"w") as write_file:
			json.dump(data, write_file)
		return data['user']
	
	raise HTTPException(
		status_code=404, detail=f'User not found'
	)

@router.delete('/{id}')
async def delete_user(user_id: int):

	item_found = False
	for user_idx, menu_item in enumerate(data['user']):
		if menu_item['id'] == user_id:
			item_found = True
			data['user'].pop(user_idx)
			
			with open(userData,"w") as write_file:
				json.dump(data, write_file)
			return "Data successfully updated."
	
	if not item_found:
		return "User ID not found."
	raise HTTPException(
		status_code=404, detail=f'item not found'
	)
