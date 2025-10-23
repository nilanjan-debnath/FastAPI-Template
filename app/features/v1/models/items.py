from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID

class ItemResponse(BaseModel):
    name: str
    details: str

    model_config = ConfigDict(
        from_attributes=True
    )  # to partially validate data from User table row

class NewItemInput(BaseModel):
    name: str = Field(..., description="Enter the name of the item")
    details: str|None = Field(None, description="Item Details")

class UpdateItemInput(BaseModel):
    id: UUID
    name: str | None = None
    details: str | None = None
