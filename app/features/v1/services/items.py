from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import status
from fastapi.exceptions import HTTPException
from app.db.models import Item
from app.features.v1.models.items import ItemResponse, NewItemInput, UpdateItemInput


async def all_items(session: AsyncSession) -> list[ItemResponse]:
    stmt = select(Item)
    result = await session.execute(statement=stmt)
    items = result.scalar().all()
    if not items:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No users found"
        )


async def get_item_by_id(id: UUID, session: AsyncSession) -> ItemResponse: ...
async def create_item(item: NewItemInput, session: AsyncSession) -> ItemResponse: ...
async def update_item(item: UpdateItemInput, session: AsyncSession) -> ItemResponse: ...
async def delete_item(id: UUID, session: AsyncSession) -> None: ...
