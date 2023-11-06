from fastapi import APIRouter, HTTPException
import json
from pydantic import BaseModel
from typing import List

class Component(BaseModel):
  id: int
  name: str
  price: int

router = APIRouter()

# Establish componentData dir
componentData = 'data/component.json'

with open(componentData, 'r') as read_file:
  data = json.load(read_file)

@router.get('/')
async def read_all_component():
	return data['component']

@router.get('/component/{id}')
async def read_component(id: int):
  for component_item in data['component']:
    if component_item['id'] == id:
      return component_item
  raise HTTPException(
    status_code=404, detail=f'component not found'
  )

@router.post('/')
async def add_component(item: Component):
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
async def delete_component(component_id: int):
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
