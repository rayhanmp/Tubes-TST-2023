from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import json
from pydantic import BaseModel

class Model(BaseModel):
    id: int
    filename: str

router = APIRouter()

modelData = 'data/model.json'


with open(modelData, "r") as read_file:
    data = json.load(read_file)

@router.get("/{furniture_id}")
async def get_model(furniture_id: int):
    file = [item for item in data['model'] if item["id"] == furniture_id]
    if file:
        filename = file[0]["filename"]
        file_path = f"model/{filename}"  # Provide the correct file path
        return FileResponse(file_path, media_type="application/octet-stream", headers={"Content-Disposition": f"attachment; filename={filename}"})
    else:
        raise HTTPException(status_code=404, detail="Item ID not found")

