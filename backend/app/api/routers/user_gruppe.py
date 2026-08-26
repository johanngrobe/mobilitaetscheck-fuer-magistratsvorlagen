from typing import List
from uuid import UUID as UUIDType

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.deps import current_gemeinde_admin, current_active_user, get_async_session
from app.crud.exceptions import NotFoundError
from app.crud.user_gruppe import crud_user_gruppe
from app.models.user import User
from app.models.user_rolle import UserRolle
from app.schemas.user_gruppe import (
    UserGruppeCreate,
    UserGruppeRead,
    UserGruppeUpdate,
    GruppeUserRead,
    GruppeUserUpdate,
)

router = APIRouter()


@router.get("/users", response_model=List[GruppeUserRead])
async def get_gruppe_users(
    db: AsyncSession = Depends(get_async_session),
    admin: User = Depends(current_gemeinde_admin),
):
    result = await db.execute(
        select(User)
        .join(User.rolle)
        .where(
            User.gemeinde_id == admin.gemeinde_id,
            UserRolle.name.in_(["Verwaltung", "Politik"]),
        )
        .order_by(UserRolle.name, User.nachname, User.vorname)
    )
    users = result.scalars().all()
    return [
        GruppeUserRead(
            id=u.id,
            vorname=u.vorname,
            nachname=u.nachname,
            email=u.email,
            gruppe_id=u.gruppe_id,
            rolle_name=u.rolle.name if u.rolle else None,
        )
        for u in users
    ]


@router.patch("/users/{user_id}", response_model=GruppeUserRead)
async def set_user_gruppe(
    user_id: UUIDType,
    obj_in: GruppeUserUpdate,
    db: AsyncSession = Depends(get_async_session),
    admin: User = Depends(current_gemeinde_admin),
):
    result = await db.execute(
        select(User).where(
            User.id == user_id,
            User.gemeinde_id == admin.gemeinde_id,
        )
    )
    target_user = result.scalar_one_or_none()
    if not target_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Benutzer nicht gefunden")
    target_user.gruppe_id = obj_in.gruppe_id
    await db.commit()
    await db.refresh(target_user)
    return target_user


@router.get("", response_model=List[UserGruppeRead])
async def get_gruppen(
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    try:
        return await crud_user_gruppe.get_all(db=db, gemeinde_id=user.gemeinde_id, sort_params=[("name", "asc")])
    except NotFoundError:
        return []


@router.post("/eigene", response_model=UserGruppeRead)
async def create_eigene_gruppe(
    obj_in: UserGruppeCreate,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    """Allow any active user to create a group for their own Gemeinde/Rolle."""
    obj_in.gemeinde_id = user.gemeinde_id
    obj_in.rolle_id = user.rolle_id
    return await crud_user_gruppe.create(db=db, obj_in=obj_in)


@router.post("", response_model=UserGruppeRead)
async def create_gruppe(
    obj_in: UserGruppeCreate,
    db: AsyncSession = Depends(get_async_session),
    admin: User = Depends(current_gemeinde_admin),
):
    obj_in.gemeinde_id = admin.gemeinde_id
    # rolle_id is passed from the request body
    return await crud_user_gruppe.create(db=db, obj_in=obj_in)


@router.patch("/{id}", response_model=UserGruppeRead)
async def update_gruppe(
    id: int,
    obj_in: UserGruppeUpdate,
    db: AsyncSession = Depends(get_async_session),
    _: User = Depends(current_gemeinde_admin),
):
    return await crud_user_gruppe.update(db=db, id=id, obj_in=obj_in)


@router.delete("/{id}", status_code=204)
async def delete_gruppe(
    id: int,
    db: AsyncSession = Depends(get_async_session),
    _: User = Depends(current_gemeinde_admin),
):
    await crud_user_gruppe.delete(db=db, id=id)
