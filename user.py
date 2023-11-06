from fastapi import APIRouter, HTTPException
import json
from pydantic import BaseModel

class User(BaseModel):
  id: int
  username: str
  password: str
  fullname: str
  address: str

router = APIRouter()

# Establish userData dir
userData = 'data/user.json'

with open(userData, 'r') as read_file:
  data = json.load(read_file)

@router.get('/')
async def read_all_user():
	return data['user']

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
	item_found = False
	for user_item in data['user']:
		if user_item['id'] == item_dict['id']:
			item_found = True
			return "User already exist."
	
	if not item_found:
		data['user'].append(item_dict)
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
