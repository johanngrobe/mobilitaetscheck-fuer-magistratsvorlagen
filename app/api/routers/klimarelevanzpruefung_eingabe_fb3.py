from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.klimarelevanzpruefung_eingabe_fb3 import (
    crud_klimarelevanzpruefung_eingabe_fb3 as crud,
)
from app.core.deps import current_active_user, get_async_session
from app.schemas.klimarelevanzpruefung_eingabe_fb3 import (
    KlimarelevanzpruefungEingabeFb3Create as CreateSchema,
    KlimarelevanzpruefungEingabeFb3Update as UpdateSchema,
    KlimarelevanzpruefungEingabeFb3Read as ReadSchema,
)

router = APIRouter()


@router.get(
    "", response_model=List[ReadSchema], dependencies=[Depends(current_active_user)]
)
async def get_klimarelevanzpruefung_eingabe_fb3(
    db: AsyncSession = Depends(get_async_session),
):
    return await crud.get_all(db)


@router.get(
    "/{id}",
    response_model=ReadSchema,
    dependencies=[Depends(current_active_user)],
)
async def get_klimarelevanzpruefung_eingabe_fb3(
    id: int, db: AsyncSession = Depends(get_async_session)
):
    return await crud.get(db, id)


@router.post(
    "",
    response_model=ReadSchema,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(current_active_user)],
)
async def create_klimarelevanzpruefung_eingabe_fb3(
    obj_in: CreateSchema, db: AsyncSession = Depends(get_async_session)
):
    return await crud.create(db, obj_in)


@router.patch(
    "/{id}",
    response_model=ReadSchema,
    dependencies=[Depends(current_active_user)],
)
async def update_klimarelevanzpruefung_eingabe_fb3(
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
async def delete_klimarelevanzpruefung_eingabe_fb3(
    id: int, db: AsyncSession = Depends(get_async_session)
):
    return await crud.delete(db, id)
