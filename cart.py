from fastapi import APIRouter, HTTPException, Depends
import json
from pydantic import BaseModel
from typing import List
from furniture import Furniture
import requests
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

class Cart(BaseModel):
  user_id: int
  items: List[Furniture]
  total_price: int

router = APIRouter()

# Establish cartData dir
cartData = 'data/cart.json'

with open(cartData, 'r') as read_file:
  data = json.load(read_file)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')
@router.get('/')
async def read_all_cart(token: str = Depends(oauth2_scheme)):
	return data['cart']

@router.get('/{user_id}')
async def read_cart(user_id: int, token: str = Depends(oauth2_scheme)):
  for cart_item in data['cart']:
    if cart_item['user_id'] == user_id:
      return cart_item
  raise HTTPException(
    status_code=404, detail=f'Cart not found'
  )

@router.post('/')
async def add_item_to_cart(user_id: int, item: Furniture, token: str = Depends(oauth2_scheme)):
    item_dict = item.dict()

    total_price = item_dict['baseprice']
    for component in item_dict['extras']:
        total_price += component['price']
     
    for cart in data['cart']:
        if cart['user_id'] == user_id:
            for existing_item in cart['items']:
                if existing_item['id'] == item_dict['id']:
                    return "Furniture item with the same ID already exists in the cart"
            
            cart['items'].append(item_dict)
            cart['total_price'] += total_price

            with open(cartData, "w") as write_file:
                json.dump(data, write_file)

            return "Furniture has been added to the cart."

    return "User not found"


@router.delete('/{user_id}/{furniture_id}')
async def delete_cart_item(user_id: int, furniture_id: int, token: str = Depends(oauth2_scheme)):
    for cart in data['cart']:
        if cart['user_id'] == user_id:
            for item in cart['items']:
                if item['id'] == furniture_id:
                    total_price = item['baseprice']
                    for component in item['extras']:
                        total_price += component['price']
                        
                    cart['items'].remove(item)
                    cart['total_price'] -= total_price
                    
                    with open(cartData, "w") as write_file:
                        json.dump(data, write_file)
                    
                    return f"Furniture item has been removed from the cart"
    
    return "User or furniture item not found"
