from fastapi import APIRouter, HTTPException, Depends, requests
import json
from pydantic import BaseModel
from typing import List
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

class Component(BaseModel):
  id: int
  name: str
  price: int

router = APIRouter()

# Establish componentData dir
componentData = 'data/component.json'
CUSGAN_API_BASE_URL = "https://customizefragrance.azurewebsites.net/" 

with open(componentData, 'r') as read_file:
  data = json.load(read_file)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')
@router.get('/')
async def read_all_component(token: str = Depends(oauth2_scheme)):
	return data['component']

@router.get('/component/{id}')
async def read_component(id: int, token: str = Depends(oauth2_scheme)):
  for component_item in data['component']:
    if component_item['id'] == id:
      return component_item
  raise HTTPException(
    status_code=404, detail=f'component not found'
  )

@router.post('/')
async def add_component(item: Component, token: str = Depends(oauth2_scheme)):
	item_dict = item.dict()
	item_found = False
	for component_item in data['component']:
		if component_item['id'] == item_dict['id']:
			item_found = True
			return "Component already exist."
	
	if not item_found:
		data['component'].append(item_dict)
		with open(componentData,"w") as write_file:
			json.dump(data, write_file)

		return item_dict
	raise HTTPException(
		status_code=404, detail=f'User not found'
	)

@router.delete('/{component_id}')
async def delete_component(component_id: int, token: str = Depends(oauth2_scheme)):
    item_found = False
    for component_idx, component_item in enumerate(data['component']):
        if component_item['id'] == component_id:
            item_found = True
            data['component'].pop(component_idx)

            with open(componentData,"w") as write_file:
                json.dump(data, write_file)
            return "Data successfully updated."

    if not item_found:
        raise HTTPException(
            status_code=404, detail=f'Component ID not found.'
        )

@router.get('/woodscent/{user_id}')
async def read_woodscent( user_id: int, token: str = Depends(oauth2_scheme),):
    
    token_res = requests.post(f"{CUSGAN_API_BASE_URL}/token", data={"username": "testinguser", "password": "testingpassword"})
    print(token_res)
    if token_res.status_code == 200:
        token_for_integration = token_res.json().get("access_token")
        
        response = requests.get(f"{CUSGAN_API_BASE_URL}/personality/{user_id}", headers={"Authorization": f"Bearer {token_for_integration}"})
        
        if response.status_code == 200:
            user_data = response.json()
            kombinasi_fragrance = user_data.get("Kombinasi_Fragrance", [])
            return {"kombinasi_fragrance": kombinasi_fragrance}
        else:
            raise HTTPException(status_code=response.status_code, detail="Error fetching user personality data.")
    else:
        raise HTTPException(status_code=token_res.status_code, detail="Error getting token.")
