from typing import List

from fastapi import APIRouter, Depends, status, Response
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.gemeinde_einheit import crud_gemeinde_einheit as crud
from app.core.deps import current_active_user, get_async_session
from app.models.user import User
from app.schemas.gemeinde_einheit import (
    GemeindeEinheitCreate as CreateSchema,
    GemeindeEinheitUpdate as UpdateSchema,
    GemeindeEinheitRead as ReadSchema,
)
from app.utils.auth_util import check_user_authorization

router = APIRouter()


@router.get("", response_model=List[ReadSchema])
async def get_gemeinde_einheit(
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    sort_params = [("name", "desc")]

    return await crud.get_by_multi_keys(
        db=db,
        keys={"gemeinde_id": user.gemeinde_id, "rolle_id": user.rolle_id},
        sort_params=sort_params,
    )


@router.get(
    "/magistratsvorlage/{magistratsvorlage_id}",
    response_model=List[ReadSchema],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(current_active_user)],
)
async def get_klimacheck(
    magistratsvorlage_id: int,
    db: AsyncSession = Depends(get_async_session),
):
    sort_params = [("erstellt_am", "desc")]

    instances = await crud.get_by_key(
        db=db,
        key="magistratsvorlage_id",
        value=magistratsvorlage_id,
        sort_params=sort_params,
    )

    if not instances:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    return instances


@router.post("", status_code=status.HTTP_201_CREATED, response_model=ReadSchema)
async def create_gemeinde_einheit(
    submission: CreateSchema,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):

    return await crud.create(db, submission, user)


@router.patch("/{id}", response_model=ReadSchema)
async def update_gemeinde_einheit(
    id: int,
    updates: UpdateSchema,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    instance = await crud.get(db, id)
    check_user_authorization(user, instance.gemeinde_id)
    return await crud.update(db, id, updates, user)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_gemeinde_einheit(
    id: int,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    instance = await crud.get(db, id)
    check_user_authorization(user, instance.gemeinde_id)
    await crud.delete(db, id)
