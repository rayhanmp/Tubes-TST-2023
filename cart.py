from fastapi import APIRouter, HTTPException
import json
from pydantic import BaseModel
from typing import List
from furniture import Furniture

class Cart(BaseModel):
  user_id: int
  items: List[Furniture]
  total_price: int

router = APIRouter()

# Establish cartData dir
cartData = 'data/cart.json'

with open(cartData, 'r') as read_file:
  data = json.load(read_file)

@router.get('/cart')
async def read_all_cart():
	return data['cart']

@router.get('/cart/{id}')
async def read_cart(id: int):
  for cart_item in data['cart']:
    if cart_item['user_id'] == id:
      return cart_item
  raise HTTPException(
    status_code=404, detail=f'Cart not found'
  )

@router.post('/cart')
async def add_cart(item: Furniture):
    item_dict = item.dict()
    item_found = False
    for cart_item in data['cart']:
        for existing_item in cart_item['items']:
            if existing_item['id'] == item_dict['id']:
                item_found = True
                break

    if not item_found:
        data['cart'][0]['items'].append(item_dict)
        data['cart'][0]['total_price'] += item_dict['baseprice']

    with open(cartData, "w") as write_file:
        json.dump(data, write_file)

    return item_dict

@router.delete('/cart/{user_id}/{furniture_id}')
async def delete_cart_item(user_id: int, furniture_id: int):
    cart_item_found = False
    cart_item = data['cart']

    if cart_item['user_id'] == user_id:
        for item in cart_item['items']:
            if item['id'] == furniture_id:
                cart_item_found = True
                cart_item['items'].remove(item)
                cart_item['total_price'] -= item['baseprice']
                break

    if cart_item_found:
        with open(cartData, "w") as write_file:
            json.dump(data, write_file)
        return f"Furniture item with ID {furniture_id} removed from the cart."
    else:
        raise HTTPException(
            status_code=404, detail=f'User or furniture not found'
        )
