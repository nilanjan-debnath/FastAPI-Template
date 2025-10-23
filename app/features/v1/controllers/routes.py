from fastapi import APIRouter, status, HTTPException
from app.features.v1.models.items import ItemResponse, UpdateItemInput, NewItemInput
from app.features.v1.services import (
    all_users,
    get_user,
    delete_user,
    create_user,
    update_user,
)
from app.db.core import DbSession


router = APIRouter(prefix="/api/v1/items", tags=["user", "v1"])


@router.get("/", response_model=list[ItemResponse], status_code=status.HTTP_200_OK)
async def get_all_users(session: DbSession) -> list[ItemResponse]:
    try:
        return await all_users(session=session)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {e}",
        )


@router.get("/{username}", response_model=ItemResponse, status_code=status.HTTP_200_OK)
async def get_user_by_id(session: DbSession, username: str) -> ItemResponse:
    try:
        return await get_user(session=session, username=username)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {e}",
        )


@router.post("/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
async def create_new_user(
    session: DbSession, user_create: NewItemInput
) -> ItemResponse:
    try:
        return await create_user(session=session, user_create=user_create)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {e}",
        )


@router.patch(
    "/{username}", response_model=ItemResponse, status_code=status.HTTP_200_OK
)
async def update_existing_user(
    session: DbSession, username: str, user_update: UpdateItemInput
) -> ItemResponse:
    try:
        return await update_user(
            session=session, username=username, user_update=user_update
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {e}",
        )


@router.delete("/{username}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_by_id(session: DbSession, username: str) -> None:
    try:
        return await delete_user(session=session, username=username)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {e}",
        )
