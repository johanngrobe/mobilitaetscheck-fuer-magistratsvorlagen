from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.bool_erweitert import (
    crud_bool_erweitert as crud,
)
from app.core.deps import current_active_user, get_async_session
from app.schemas.bool_erweitert import (
    BoolErweitertCreate as CreateSchema,
    BoolErweitertUpdate as UpdateSchema,
    BoolErweitertRead as ReadSchema,
)

router = APIRouter()


@router.get(
    "", response_model=List[ReadSchema], dependencies=[Depends(current_active_user)]
)
async def get_bool_erweitert(
    db: AsyncSession = Depends(get_async_session),
):
    return await crud.get_all(db)


@router.get(
    "/{id}",
    response_model=ReadSchema,
    dependencies=[Depends(current_active_user)],
)
async def get_bool_erweitert(id: int, db: AsyncSession = Depends(get_async_session)):
    return await crud.get(db, id)


@router.post(
    "",
    response_model=ReadSchema,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(current_active_user)],
)
async def create_bool_erweitert(
    obj_in: CreateSchema, db: AsyncSession = Depends(get_async_session)
):
    return await crud.create(db, obj_in)


@router.patch(
    "/{id}",
    response_model=ReadSchema,
    dependencies=[Depends(current_active_user)],
)
async def update_bool_erweitert(
    id: int,
    updates: UpdateSchema,
    db: AsyncSession = Depends(get_async_session),
):
    return await crud.update(db, id, updates)


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(current_active_user)],
)
async def delete_bool_erweitert(id: int, db: AsyncSession = Depends(get_async_session)):
    return await crud.delete(db, id)
