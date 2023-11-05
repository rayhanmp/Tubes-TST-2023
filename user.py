from fastapi import FastAPI, HTTPException
import json
from pydantic import BaseModel

class User(BaseModel):
  id: int
  username: str
  password: str
  fullname: str
  address: str

app = FastAPI()

# Establish userData dir
userData = 'data/user.json'

with open(userData, 'r') as read_file:
  data = json.load(read_file)

@app.get('/user')
async def read_all_user():
	return data['user']

@app.get('/user/{id}')
async def read_user(id: int):
  for user_item in data['user']:
    if user_item['id'] == id:
      return user_item
  raise HTTPException(
    status_code=404, detail=f'User not found'
  )

@app.post('/user')
async def add_user(item: Item):
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

		return item_dict
	raise HTTPException(
		status_code=404, detail=f'User not found'
	)

@app.delete('/user/{id}')
async def delete_user(user_id: int):

	item_found = False
	for menu_idx, menu_item in enumerate(data['user']):
		if menu_item['id'] == user_id:
			item_found = True
			data['user'].pop(user_idx)
			
			with open(json_filename,"w") as write_file:
				json.dump(data, write_file)
			return "Data successfully updated."
	
	if not item_found:
		return "User ID not found."
	raise HTTPException(
		status_code=404, detail=f'item not found'
	)