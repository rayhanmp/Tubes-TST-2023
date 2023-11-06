# MICROSERVICE DEPLOYMENT: GAMIFIED CUSTOM FURNITURE

## Core Service
This service aims to provide gamified experience when deciding their custom furniture. In the next continuation of the project, ThreeJS will be used as WebGL library to render and manipulate the 3D image. The service will display and calculate the final price for the user based on customizable extra components.

## Tech Used
- **Python** 3.11
- **Uvicorn** 0.23.2
- **Pydantic** 2.4.2
- **FastAPI** 0.104.1

## Feature
- CRUD user
- CRUD furniture
- CRUD component
- Get gltf model for furniture
- Get total price in the cart

## How to Use
1. Open [tstfastapi.azurewebsites.net/docs#/](https://tstfastapi.azurewebsites.net/docs#/)
2. Try all the API presented by the FastAPI documentation
3. Alternatively, you can build the docker image and run it on your local machine using the command `docker build  -t myimage` and then `docker run -d --name mycontainer -p 80:80 myimage`

## API Endpoint
| Methods | URI | Description    |
| :---:| :---:   | :---: |
| **GET**|  https://tstfastapi.azurewebsites.net/user/ | Get all the user data |
| **GET**|  https://tstfastapi.azurewebsites.net/user/{id} | Get the data of a specific user |
| **POST**|  https://tstfastapi.azurewebsites.net/user/ | Make a new user data |
| **DELETE**|  https://tstfastapi.azurewebsites.net/user/{id} | Delete a specific user data |
| **GET**|  https://tstfastapi.azurewebsites.net/component/ | Get all the component data |
| **POST**|  https://tstfastapi.azurewebsites.net/component/ | Make a new component data |
| **GET**|  https://tstfastapi.azurewebsites.net/component/component/{id} | Get the data of a specific component |
| **DELETE**|  https://tstfastapi.azurewebsites.net/component/{component_id} | Delete a specific furniture data |
| **GET**|  https://tstfastapi.azurewebsites.net/furniture/ | Get all the furniture data |
| **POST**|  https://tstfastapi.azurewebsites.net/furniture/ | Make a new furniture data |
| **GET**|  https://tstfastapi.azurewebsites.net/furniture/{id} | Get the data of a specific furniture |
| **DELETE**|  https://tstfastapi.azurewebsites.net/furniture/{furniture_id} | Delete a specific furniture data |
| **GET**|  https://tstfastapi.azurewebsites.net/cart/ | Get all the cart data |
| **POST**|  https://tstfastapi.azurewebsites.net/cart/{user_id}/{furniture_id} | Insert a specific furniture to a cart |
| **GET**|  https://tstfastapi.azurewebsites.net/cart/{user_id} | Get the data of a specific cart based on user id |
| **DELETE**|  https://tstfastapi.azurewebsites.net/cart/{user_id}/furniture_id} | Delete a specific furniture from a cart |
| **GET**|  https://tstfastapi.azurewebsites.net/model/{furniture_id} | Get the gltf model of a specific furniture |

## Notes
There is a bug that makes the API call returns the message of "an item not found" or "item already exists", however **it doesn't actually affect the functionality.**
## Author
Project by **18221130** Rayhan Maheswara Pramanda.
