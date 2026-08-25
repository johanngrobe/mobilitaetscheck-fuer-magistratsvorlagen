from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from jose import JWTError
from pydantic import BaseModel, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.config import settings
from app.core.deps import get_async_session, get_user_manager
from app.crud.exceptions import NotFoundError
from app.crud.mobilitaetscheck_eingabe import crud_mobility_submission
from app.crud.plattform_einstellung import crud_plattform_einstellung
from app.crud.user import crud_user as crud
from app.models.gemeinde import Gemeinde
from app.models.magistratsvorlage import Magistratsvorlage
from app.models.mobilitaetscheck_eingabe import MobilitaetscheckEingabe
from app.models.user import User
from app.models.user_rolle import UserRolle
from app.schemas.gemeinde import GemeindeRead
from app.schemas.magistratsvorlage import MagistratsvorlageRead
from app.schemas.mobilitaetscheck_eingabe import MobilitaetscheckEingabeRead
from app.schemas.plattform_einstellung import PlattformEinstellungRead
from app.schemas.user import UserCreate
from app.services.user.user_manager import UserManager
from app.utils.invite_token import decode_invite_token

router = APIRouter()

ADMIN_ROLLE_NAME = "Admin"
SYSTEM_GEMEINDE_NAME = "Systemadministration"


class SetupCreate(BaseModel):
    vorname: str
    nachname: str
    email: EmailStr
    password: str


@router.get("/setup-status")
async def get_setup_status(db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(
        select(User)
        .join(UserRolle, User.rolle_id == UserRolle.id)
        .where(User.is_superuser == True, UserRolle.name == ADMIN_ROLLE_NAME)
    )
    admin = result.scalar_one_or_none()
    return {"needs_setup": admin is None}


@router.post("/setup", status_code=201)
async def setup(
    obj_in: SetupCreate,
    db: AsyncSession = Depends(get_async_session),
    user_manager: UserManager = Depends(get_user_manager),
):
    # Guard: only allowed if no Platform Admin exists yet
    result = await db.execute(
        select(User)
        .join(UserRolle, User.rolle_id == UserRolle.id)
        .where(User.is_superuser == True, UserRolle.name == ADMIN_ROLLE_NAME)
    )
    if result.scalar_one_or_none() is not None:
        raise HTTPException(status_code=409, detail="Systemadministrator existiert bereits.")

    rolle_result = await db.execute(
        select(UserRolle).where(UserRolle.name == ADMIN_ROLLE_NAME)
    )
    admin_rolle = rolle_result.scalar_one_or_none()
    if admin_rolle is None:
        raise HTTPException(status_code=500, detail="Admin-Rolle nicht gefunden.")

    gemeinde_result = await db.execute(
        select(Gemeinde).where(Gemeinde.name == SYSTEM_GEMEINDE_NAME)
    )
    system_gemeinde = gemeinde_result.scalar_one_or_none()
    if system_gemeinde is None:
        raise HTTPException(status_code=500, detail="System-Gemeinde nicht gefunden.")

    user_create = UserCreate(
        email=obj_in.email,
        password=obj_in.password,
        vorname=obj_in.vorname,
        nachname=obj_in.nachname,
        rolle_id=admin_rolle.id,
        gemeinde_id=system_gemeinde.id,
        is_superuser=True,
        is_verified=True,
    )
    await user_manager.create(user_create, safe=False)
    return {"detail": "Systemadministrator wurde erfolgreich erstellt."}


from app.models.user_gruppe import UserGruppe
from app.schemas.user_gruppe import UserGruppeRead


class EinladungInfo(BaseModel):
    email: str
    gemeinde_id: int
    gemeinde_name: str
    rolle_id: int
    rolle_name: str


@router.get(
    "/unique-email",
)
async def get_unique_email(
    email: str,
    db: AsyncSession = Depends(get_async_session),
):
    try:
        instance = await crud.get_by_key(
            db=db,
            key="email",
            value=email,
        )
    except NotFoundError:
        instance = None
    return {"email_gueltig": instance is None}


@router.get("/gruppen", response_model=list[UserGruppeRead])
async def get_public_gruppen(
    gemeinde_id: int,
    rolle_id: int,
    db: AsyncSession = Depends(get_async_session),
):
    result = await db.execute(
        select(UserGruppe)
        .where(UserGruppe.gemeinde_id == gemeinde_id, UserGruppe.rolle_id == rolle_id)
        .order_by(UserGruppe.name)
    )
    return result.scalars().all()


@router.get("/einladung/{token}", response_model=EinladungInfo)
async def get_einladung_info(
    token: str,
    db: AsyncSession = Depends(get_async_session),
):
    try:
        payload = decode_invite_token(token, settings.EINLADUNG_TOKEN_SECRET)
    except JWTError:
        raise HTTPException(
            status_code=400, detail="Der Einladungslink ist ungültig oder abgelaufen."
        )

    gemeinde_result = await db.execute(
        select(Gemeinde).where(Gemeinde.id == payload["gemeinde_id"])
    )
    gemeinde = gemeinde_result.scalar_one_or_none()

    rolle_result = await db.execute(
        select(UserRolle).where(UserRolle.id == payload["rolle_id"])
    )
    rolle = rolle_result.scalar_one_or_none()

    if gemeinde is None or rolle is None:
        raise HTTPException(status_code=400, detail="Ungültige Einladungsdaten.")

    return EinladungInfo(
        email=payload["email"],
        gemeinde_id=gemeinde.id,
        gemeinde_name=gemeinde.name,
        rolle_id=rolle.id,
        rolle_name=rolle.name,
    )


# ---------------------------------------------------------------------------
# Public read-only access (no authentication required)
# ---------------------------------------------------------------------------

@router.get("/plattform-einstellung", response_model=PlattformEinstellungRead)
async def get_public_plattform_einstellung(db: AsyncSession = Depends(get_async_session)):
    """Return the Datenschutzerklärung and other public platform settings."""
    return await crud_plattform_einstellung.get(db)


@router.get("/gemeinden", response_model=list[GemeindeRead])
async def get_public_gemeinden(db: AsyncSession = Depends(get_async_session)):
    """Return all Gemeinden except the internal Systemadministration gemeinde."""
    result = await db.execute(
        select(Gemeinde)
        .where(Gemeinde.name != SYSTEM_GEMEINDE_NAME)
        .order_by(Gemeinde.name)
    )
    return result.scalars().all()


@router.get("/magistratsvorlage", response_model=list[MagistratsvorlageRead])
async def get_public_magistratsvorlagen(
    gemeinde_id: int,
    db: AsyncSession = Depends(get_async_session),
):
    """Return published Magistratsvorlagen for a Gemeinde."""
    result = await db.execute(
        select(Magistratsvorlage)
        .where(
            Magistratsvorlage.gemeinde_id == gemeinde_id,
            Magistratsvorlage.veroeffentlicht == True,
        )
        .order_by(Magistratsvorlage.erstellt_am.desc())
    )
    return result.scalars().all()


@router.get("/magistratsvorlage/{id}", response_model=MagistratsvorlageRead)
async def get_public_magistratsvorlage(
    id: int,
    db: AsyncSession = Depends(get_async_session),
):
    """Return a single published Magistratsvorlage."""
    result = await db.execute(
        select(Magistratsvorlage).where(
            Magistratsvorlage.id == id,
            Magistratsvorlage.veroeffentlicht == True,
        )
    )
    instance = result.scalar_one_or_none()
    if instance is None:
        raise HTTPException(status_code=404, detail="Magistratsvorlage nicht gefunden.")
    return instance


@router.get(
    "/mobilitaetscheck/magistratsvorlage/{magistratsvorlage_id}",
    response_model=list[MobilitaetscheckEingabeRead],
)
async def get_public_mobilitaetschecks(
    magistratsvorlage_id: int,
    db: AsyncSession = Depends(get_async_session),
):
    """Return published Mobilitätschecks for a published Magistratsvorlage."""
    # Verify the Magistratsvorlage itself is published
    mv_result = await db.execute(
        select(Magistratsvorlage).where(
            Magistratsvorlage.id == magistratsvorlage_id,
            Magistratsvorlage.veroeffentlicht == True,
        )
    )
    if mv_result.scalar_one_or_none() is None:
        raise HTTPException(status_code=404, detail="Magistratsvorlage nicht gefunden.")

    result = await db.execute(
        select(MobilitaetscheckEingabe)
        .where(
            MobilitaetscheckEingabe.magistratsvorlage_id == magistratsvorlage_id,
            MobilitaetscheckEingabe.veroeffentlicht == True,
        )
        .order_by(MobilitaetscheckEingabe.erstellt_am.desc())
    )
    return result.scalars().all()


@router.get("/mobilitaetscheck/export/{id}")
async def export_public_mobilitaetscheck(
    id: int,
    db: AsyncSession = Depends(get_async_session),
):
    """Export a published Mobilitätscheck as PDF (no auth required)."""
    result = await db.execute(
        select(MobilitaetscheckEingabe).where(
            MobilitaetscheckEingabe.id == id,
            MobilitaetscheckEingabe.veroeffentlicht == True,
        )
    )
    if result.scalar_one_or_none() is None:
        raise HTTPException(status_code=404, detail="Mobilitätscheck nicht gefunden.")

    pdf_export = await crud_mobility_submission.export(db, id)
    filename = f"mobilitaetscheck_{id}.pdf"
    headers = {"Content-Disposition": f"attachment; filename={filename}"}
    return StreamingResponse(pdf_export, media_type="application/pdf", headers=headers)
