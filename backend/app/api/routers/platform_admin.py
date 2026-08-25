from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID

from app.core.deps import current_platform_admin, get_async_session
from app.crud.exceptions import NotFoundError
from app.crud.email_vorlage import crud_email_vorlage
from app.crud.gemeinde import crud_gemeinde
from app.crud.plattform_einstellung import crud_plattform_einstellung
from app.models.user import User
from app.models.gemeinde import Gemeinde
from app.schemas.email_vorlage import EmailVorlageRead, EmailVorlageUpdate
from app.schemas.gemeinde import GemeindeCreate, GemeindeRead, GemeindeUpdate
from app.schemas.plattform_einstellung import (
    PlattformEinstellungRead,
    PlattformEinstellungUpdate,
)
from app.schemas.user import UserRead
from app.services.mail.vorlagen_registry import DEFAULT_VORLAGEN, get_default_inhalt

router = APIRouter()


def _to_email_vorlage_read(instance) -> EmailVorlageRead:
    default = DEFAULT_VORLAGEN[instance.key]
    return EmailVorlageRead(
        key=instance.key,
        betreff=instance.betreff,
        inhalt=instance.inhalt,
        standard_betreff=default["betreff"],
        standard_inhalt=get_default_inhalt(instance.key),
        platzhalter=default["platzhalter"],
    )


@router.get("/email-vorlage", response_model=List[EmailVorlageRead])
async def get_all_email_vorlagen(
    db: AsyncSession = Depends(get_async_session),
    _: User = Depends(current_platform_admin),
):
    instances = await crud_email_vorlage.get_all(db)
    return [_to_email_vorlage_read(i) for i in instances]


@router.patch("/email-vorlage/{key}", response_model=EmailVorlageRead)
async def update_email_vorlage(
    key: str,
    obj_in: EmailVorlageUpdate,
    db: AsyncSession = Depends(get_async_session),
    _: User = Depends(current_platform_admin),
):
    if key not in DEFAULT_VORLAGEN:
        raise HTTPException(status_code=404, detail="Email-Vorlage nicht gefunden.")
    instance = await crud_email_vorlage.update(db, key, obj_in)
    return _to_email_vorlage_read(instance)


@router.post("/email-vorlage/{key}/reset", response_model=EmailVorlageRead)
async def reset_email_vorlage(
    key: str,
    db: AsyncSession = Depends(get_async_session),
    _: User = Depends(current_platform_admin),
):
    if key not in DEFAULT_VORLAGEN:
        raise HTTPException(status_code=404, detail="Email-Vorlage nicht gefunden.")
    instance = await crud_email_vorlage.reset(db, key)
    return _to_email_vorlage_read(instance)


@router.get("/einstellung", response_model=PlattformEinstellungRead)
async def get_plattform_einstellung(
    db: AsyncSession = Depends(get_async_session),
    _: User = Depends(current_platform_admin),
):
    return await crud_plattform_einstellung.get(db)


@router.patch("/einstellung", response_model=PlattformEinstellungRead)
async def update_plattform_einstellung(
    obj_in: PlattformEinstellungUpdate,
    db: AsyncSession = Depends(get_async_session),
    _: User = Depends(current_platform_admin),
):
    return await crud_plattform_einstellung.update(db, obj_in)


@router.get("/gemeinde", response_model=List[GemeindeRead])
async def get_all_gemeinden(
    db: AsyncSession = Depends(get_async_session),
    _: User = Depends(current_platform_admin),
):
    try:
        return await crud_gemeinde.get_all(db=db, sort_params=[("name", "asc")])
    except NotFoundError:
        return []


@router.post("/gemeinde", response_model=GemeindeRead)
async def create_gemeinde(
    obj_in: GemeindeCreate,
    db: AsyncSession = Depends(get_async_session),
    _: User = Depends(current_platform_admin),
):
    return await crud_gemeinde.create(db=db, obj_in=obj_in)


@router.patch("/gemeinde/{id}", response_model=GemeindeRead)
async def update_gemeinde(
    id: int,
    obj_in: GemeindeUpdate,
    db: AsyncSession = Depends(get_async_session),
    _: User = Depends(current_platform_admin),
):
    return await crud_gemeinde.update(db=db, id=id, obj_in=obj_in)


@router.delete("/gemeinde/{id}", status_code=204)
async def delete_gemeinde(
    id: int,
    db: AsyncSession = Depends(get_async_session),
    _: User = Depends(current_platform_admin),
):
    await crud_gemeinde.delete(db=db, id=id)


class UserAdminUpdate(BaseModel):
    rolle_id: Optional[int] = Field(None)
    gemeinde_id: Optional[int] = Field(None)
    is_superuser: Optional[bool] = Field(None)


@router.get("/user", response_model=List[UserRead])
async def get_all_users(
    db: AsyncSession = Depends(get_async_session),
    _: User = Depends(current_platform_admin),
):
    result = await db.execute(select(User))
    return list(result.scalars().all())


@router.delete("/user/{user_id}", status_code=204)
async def delete_user_by_admin(
    user_id: UUID,
    db: AsyncSession = Depends(get_async_session),
    _: User = Depends(current_platform_admin),
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="Benutzer nicht gefunden")
    await db.delete(user)
    await db.commit()


@router.patch("/user/{user_id}", response_model=UserRead)
async def update_user_by_admin(
    user_id: UUID,
    obj_in: UserAdminUpdate,
    db: AsyncSession = Depends(get_async_session),
    _: User = Depends(current_platform_admin),
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="Benutzer nicht gefunden")
    if obj_in.rolle_id is not None:
        user.rolle_id = obj_in.rolle_id
    if obj_in.gemeinde_id is not None:
        user.gemeinde_id = obj_in.gemeinde_id
    if obj_in.is_superuser is not None:
        user.is_superuser = obj_in.is_superuser
    await db.commit()
    await db.refresh(user)
    return user
