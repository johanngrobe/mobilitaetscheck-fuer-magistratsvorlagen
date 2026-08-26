from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.config import settings
from app.core.deps import current_active_user, get_async_session
from app.models.gemeinde import Gemeinde
from app.models.user import User
from app.models.user_rolle import UserRolle
from app.services.mail.messages import send_einladung
from app.utils.invite_token import create_invite_token

router = APIRouter()

ADMIN_ROLLE_NAME = "Admin"
POLITIK_ROLLE_NAME = "Politik"


class EinladungCreate(BaseModel):
    email: EmailStr = Field(..., description="E-Mail-Adresse der eingeladenen Person")
    rolle_id: int = Field(..., description="Rolle der eingeladenen Person")
    gueltig_stunden: int = Field(72, ge=1, description="Gültigkeitsdauer in Stunden")
    gemeinde_id: Optional[int] = Field(None, description="Nur für Platform-Admins: Ziel-Gemeinde")
    is_superuser: bool = Field(False, description="Nur für Platform-Admins: Gemeinde-Admin einladen")


@router.post("")
async def create_einladung(
    obj_in: EinladungCreate,
    db: AsyncSession = Depends(get_async_session),
    admin: User = Depends(current_active_user),
):
    is_platform_admin = admin.is_superuser and admin.rolle.name == ADMIN_ROLLE_NAME
    is_gemeinde_admin = admin.is_superuser and admin.rolle.name != ADMIN_ROLLE_NAME
    is_politik = not admin.is_superuser and admin.rolle.name == POLITIK_ROLLE_NAME

    if not is_platform_admin and not is_gemeinde_admin and not is_politik:
        raise HTTPException(status_code=403, detail="Keine Berechtigung")

    result = await db.execute(
        select(UserRolle).where(UserRolle.id == obj_in.rolle_id)
    )
    rolle = result.scalar_one_or_none()
    if rolle is None:
        raise HTTPException(status_code=404, detail="Rolle nicht gefunden")

    # Politik users can only invite other Politik users
    if is_politik and rolle.name != POLITIK_ROLLE_NAME:
        raise HTTPException(status_code=403, detail="Politik-Benutzer können nur Politik-Benutzer einladen")

    # Only Platform-Admins may invite someone into the Admin (Systemadmin) role
    if not is_platform_admin and rolle.name == ADMIN_ROLLE_NAME:
        raise HTTPException(status_code=403, detail="Nur Systemadministratoren können neue Systemadministratoren einladen")

    if is_platform_admin:
        if obj_in.gemeinde_id is None:
            raise HTTPException(status_code=400, detail="gemeinde_id ist erforderlich")
        target_gemeinde_id = obj_in.gemeinde_id
        invite_is_superuser = obj_in.is_superuser
        gemeinde_result = await db.execute(select(Gemeinde).where(Gemeinde.id == target_gemeinde_id))
        target_gemeinde = gemeinde_result.scalar_one_or_none()
        if target_gemeinde is None:
            raise HTTPException(status_code=404, detail="Gemeinde nicht gefunden")
        target_gemeinde_name = target_gemeinde.name
    else:
        target_gemeinde_id = admin.gemeinde_id
        invite_is_superuser = obj_in.is_superuser if is_gemeinde_admin else False
        target_gemeinde_name = admin.gemeinde.name

    token = create_invite_token(
        email=obj_in.email,
        gemeinde_id=target_gemeinde_id,
        rolle_id=obj_in.rolle_id,
        secret=settings.EINLADUNG_TOKEN_SECRET,
        valid_hours=obj_in.gueltig_stunden,
        is_superuser=invite_is_superuser,
    )

    await send_einladung(
        email=obj_in.email,
        gemeinde_name=target_gemeinde_name,
        rolle_name=rolle.name,
        token=token,
        valid_hours=obj_in.gueltig_stunden,
    )

    return {"detail": f"Einladung an {obj_in.email} wurde gesendet."}
