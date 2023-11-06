from fastapi import APIRouter, HTTPException
import json
from pydantic import BaseModel
from typing import List
from component import Component

class Furniture(BaseModel):
  id: int
  name: str
  type: str
  color: str
  height: int
  width: int
  depth: int
  weight: int
  surface_area: int
  volume: int
  baseprice: int
  extras: List[Component]

router = APIRouter()

# Establish furnitureData dir
furnitureData = 'data/furniture.json'

with open(furnitureData, 'r') as read_file:
  data = json.load(read_file)

@router.get('/')
async def read_all_furniture():
	return data['furniture']

@router.get('/{id}')
async def read_furniture(id: int):
  for furniture_item in data['furniture']:
    if furniture_item['id'] == id:
      return furniture_item
  raise HTTPException(
    status_code=404, detail=f'Furniture not found'
  )

@router.post('/')
async def add_furniture(item: Furniture):
	item_dict = item.dict()
	item_found = False
	for furniture_item in data['furniture']:
		if furniture_item['id'] == item_dict['id']:
			item_found = True
			return "Furniture already exist."
	
	if not item_found:
		data['furniture'].append(item_dict)
		with open(furnitureData,"w") as write_file:
			json.dump(data, write_file)

		return item_dict
	raise HTTPException(
		status_code=404, detail=f'User not found'
	)

@router.delete('/{furniture_id}')
async def delete_furniture(furniture_id: int):
    item_found = False
    for furniture_idx, furniture_item in enumerate(data['furniture']):
        if furniture_item['id'] == furniture_id:
            item_found = True
            data['furniture'].pop(furniture_idx)

            with open(furnitureData,"w") as write_file:
                json.dump(data, write_file)
            return "Data successfully updated."

    if not item_found:
        raise HTTPException(
            status_code=404, detail=f'Furniture ID not found.'
        )
