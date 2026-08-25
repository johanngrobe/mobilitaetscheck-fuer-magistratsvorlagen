from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.deps import current_platform_admin, get_async_session
from app.crud.branding_bild import crud_branding_asset, crud_branding_slot_zuweisung, crud_logo_liste_eintrag
from app.models.branding_asset import BrandingAsset
from app.models.branding_slot_zuweisung import BrandingSlotZuweisung
from app.models.logo_liste_eintrag import LogoListeEintrag
from app.models.user import User
from app.schemas.branding_bild import (
    BrandingAssetRead,
    BrandingBildLinkUpdate,
    BrandingSlotAssignUpdate,
    BrandingSlotRead,
    LogoListeEintragCreate,
    LogoListeEintragRead,
    LogoListeEintragUpdate,
    LogoListeReorderUpdate,
)
from app.services.branding.slots_registry import BRANDING_SLOTS

router = APIRouter()


def _asset_url(dateiname: str) -> str:
    return f"{settings.HOST_URL}/uploads/branding/{dateiname}"


async def _is_asset_in_use(db: AsyncSession, asset_id: int) -> bool:
    zuweisung_result = await db.execute(
        select(BrandingSlotZuweisung.id).where(BrandingSlotZuweisung.asset_id == asset_id)
    )
    if zuweisung_result.scalars().first() is not None:
        return True
    listen_result = await db.execute(
        select(LogoListeEintrag.id).where(LogoListeEintrag.asset_id == asset_id)
    )
    return listen_result.scalars().first() is not None


async def _to_asset_read(db: AsyncSession, asset: BrandingAsset) -> BrandingAssetRead:
    return BrandingAssetRead(
        id=asset.id,
        url=_asset_url(asset.dateiname),
        original_dateiname=asset.original_dateiname,
        erstellt_am=asset.erstellt_am,
        in_verwendung=await _is_asset_in_use(db, asset.id),
    )


async def _to_logo_liste_eintrag_read(db: AsyncSession, instance: LogoListeEintrag) -> LogoListeEintragRead:
    return LogoListeEintragRead(
        id=instance.id,
        bereich=instance.bereich,
        asset=await _to_asset_read(db, instance.asset),
        link=instance.link,
        reihenfolge=instance.reihenfolge,
    )


async def _to_slot_read(db: AsyncSession, instance: BrandingSlotZuweisung) -> BrandingSlotRead:
    slot_info = BRANDING_SLOTS[instance.slot]
    return BrandingSlotRead(
        slot=instance.slot,
        label=slot_info["label"],
        beschreibung=slot_info["beschreibung"],
        bereich=slot_info["bereich"],
        asset=await _to_asset_read(db, instance.asset) if instance.asset_id else None,
        verlinkbar=slot_info["verlinkbar"],
        link=instance.link,
    )


@router.get("", response_model=list[BrandingSlotRead])
async def get_all_branding_slots(db: AsyncSession = Depends(get_async_session)):
    instances = await crud_branding_slot_zuweisung.get_all(db)
    return [await _to_slot_read(db, i) for i in instances]


@router.get("/assets", response_model=list[BrandingAssetRead])
async def get_all_branding_assets(
    db: AsyncSession = Depends(get_async_session),
    _: User = Depends(current_platform_admin),
):
    instances = await crud_branding_asset.get_all(db)
    return [await _to_asset_read(db, i) for i in instances]


@router.post("/assets", response_model=BrandingAssetRead)
async def upload_branding_asset(
    file: UploadFile,
    db: AsyncSession = Depends(get_async_session),
    _: User = Depends(current_platform_admin),
):
    instance = await crud_branding_asset.upload(db, file)
    return await _to_asset_read(db, instance)


@router.delete("/assets/{asset_id}", status_code=204)
async def delete_branding_asset(
    asset_id: int,
    db: AsyncSession = Depends(get_async_session),
    _: User = Depends(current_platform_admin),
):
    await crud_branding_asset.delete(db, asset_id)


@router.post("/reset", status_code=204)
async def reset_all_branding(
    db: AsyncSession = Depends(get_async_session),
    _: User = Depends(current_platform_admin),
):
    """Unassign all fixed branding slots and clear all logo lists (footer, login).
    Uploaded assets in the library are kept."""
    await crud_branding_slot_zuweisung.reset_all(db)
    await crud_logo_liste_eintrag.reset_all(db)


@router.patch("/{slot}/assign", response_model=BrandingSlotRead)
async def assign_branding_slot_asset(
    slot: str,
    obj_in: BrandingSlotAssignUpdate,
    db: AsyncSession = Depends(get_async_session),
    _: User = Depends(current_platform_admin),
):
    instance = await crud_branding_slot_zuweisung.assign_asset(db, slot, obj_in.asset_id)
    return await _to_slot_read(db, instance)


@router.patch("/{slot}/link", response_model=BrandingSlotRead)
async def update_branding_slot_link(
    slot: str,
    obj_in: BrandingBildLinkUpdate,
    db: AsyncSession = Depends(get_async_session),
    _: User = Depends(current_platform_admin),
):
    instance = await crud_branding_slot_zuweisung.update_link(db, slot, obj_in.link)
    return await _to_slot_read(db, instance)


@router.get("/logo-listen/{bereich}", response_model=list[LogoListeEintragRead])
async def get_logo_liste(bereich: str, db: AsyncSession = Depends(get_async_session)):
    instances = await crud_logo_liste_eintrag.get_all(db, bereich)
    return [await _to_logo_liste_eintrag_read(db, i) for i in instances]


@router.post("/logo-listen/{bereich}", response_model=LogoListeEintragRead)
async def create_logo_liste_eintrag(
    bereich: str,
    obj_in: LogoListeEintragCreate,
    db: AsyncSession = Depends(get_async_session),
    _: User = Depends(current_platform_admin),
):
    instance = await crud_logo_liste_eintrag.create(db, bereich, obj_in)
    return await _to_logo_liste_eintrag_read(db, instance)


@router.patch("/logo-listen/{bereich}/{eintrag_id}", response_model=LogoListeEintragRead)
async def update_logo_liste_eintrag(
    bereich: str,
    eintrag_id: int,
    obj_in: LogoListeEintragUpdate,
    db: AsyncSession = Depends(get_async_session),
    _: User = Depends(current_platform_admin),
):
    instance = await crud_logo_liste_eintrag.update(db, bereich, eintrag_id, obj_in)
    return await _to_logo_liste_eintrag_read(db, instance)


@router.delete("/logo-listen/{bereich}/{eintrag_id}", status_code=204)
async def delete_logo_liste_eintrag(
    bereich: str,
    eintrag_id: int,
    db: AsyncSession = Depends(get_async_session),
    _: User = Depends(current_platform_admin),
):
    await crud_logo_liste_eintrag.delete(db, bereich, eintrag_id)


@router.post("/logo-listen/{bereich}/reorder", response_model=list[LogoListeEintragRead])
async def reorder_logo_liste(
    bereich: str,
    obj_in: LogoListeReorderUpdate,
    db: AsyncSession = Depends(get_async_session),
    _: User = Depends(current_platform_admin),
):
    instances = await crud_logo_liste_eintrag.reorder(db, bereich, obj_in)
    return [await _to_logo_liste_eintrag_read(db, i) for i in instances]
