import uuid
from pathlib import Path

from fastapi import HTTPException, UploadFile
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.config import settings
from app.models.branding_asset import BrandingAsset
from app.models.branding_slot_zuweisung import BrandingSlotZuweisung
from app.models.logo_liste_eintrag import LogoListeEintrag
from app.schemas.branding_bild import (
    LogoListeEintragCreate,
    LogoListeEintragUpdate,
    LogoListeReorderUpdate,
)
from app.services.branding.slots_registry import (
    ALLOWED_UPLOAD_TYPES,
    BRANDING_SLOTS,
    CONTENT_TYPE_TO_EXTENSION,
    LOGO_LISTEN_BEREICHE,
    MAX_UPLOAD_SIZE_BYTES,
)

UPLOAD_DIR = Path(settings.BRANDING_UPLOAD_DIR)


class CRUDBrandingAsset:
    async def get_all(self, db: AsyncSession) -> list[BrandingAsset]:
        result = await db.execute(select(BrandingAsset).order_by(BrandingAsset.erstellt_am.desc()))
        return list(result.scalars().all())

    async def upload(self, db: AsyncSession, file: UploadFile) -> BrandingAsset:
        if file.content_type not in ALLOWED_UPLOAD_TYPES:
            raise HTTPException(
                status_code=400, detail=f"Dateityp {file.content_type} ist nicht erlaubt."
            )

        contents = await file.read()
        if len(contents) > MAX_UPLOAD_SIZE_BYTES:
            raise HTTPException(status_code=400, detail="Datei ist zu groß (max. 2 MB).")

        extension = CONTENT_TYPE_TO_EXTENSION.get(file.content_type, "bin")
        dateiname = f"{uuid.uuid4().hex}.{extension}"

        UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
        (UPLOAD_DIR / dateiname).write_bytes(contents)

        instance = BrandingAsset(
            dateiname=dateiname, original_dateiname=file.filename
        )
        db.add(instance)
        await db.commit()
        await db.refresh(instance)
        return instance

    async def delete(self, db: AsyncSession, asset_id: int) -> None:
        result = await db.execute(select(BrandingAsset).where(BrandingAsset.id == asset_id))
        instance = result.scalar_one_or_none()
        if instance is None:
            raise HTTPException(status_code=404, detail="Asset nicht gefunden.")

        zuweisung_result = await db.execute(
            select(BrandingSlotZuweisung).where(BrandingSlotZuweisung.asset_id == asset_id)
        )
        listen_result = await db.execute(
            select(LogoListeEintrag).where(LogoListeEintrag.asset_id == asset_id)
        )
        if zuweisung_result.scalars().first() is not None or listen_result.scalars().first() is not None:
            raise HTTPException(
                status_code=400,
                detail="Dieses Bild wird noch verwendet und kann nicht gelöscht werden.",
            )

        (UPLOAD_DIR / instance.dateiname).unlink(missing_ok=True)
        await db.delete(instance)
        await db.commit()


class CRUDBrandingSlotZuweisung:
    async def get_all(self, db: AsyncSession) -> list[BrandingSlotZuweisung]:
        result = await db.execute(select(BrandingSlotZuweisung))
        by_slot = {z.slot: z for z in result.scalars().all()}
        return [
            by_slot.get(slot)
            or BrandingSlotZuweisung(slot=slot, link=BRANDING_SLOTS[slot]["standard_link"])
            for slot in BRANDING_SLOTS
        ]

    async def _get_or_create(self, db: AsyncSession, slot: str) -> BrandingSlotZuweisung:
        if slot not in BRANDING_SLOTS:
            raise HTTPException(status_code=404, detail="Unbekannter Branding-Slot.")
        result = await db.execute(select(BrandingSlotZuweisung).where(BrandingSlotZuweisung.slot == slot))
        instance = result.scalar_one_or_none()
        if instance is None:
            instance = BrandingSlotZuweisung(slot=slot, link=BRANDING_SLOTS[slot]["standard_link"])
            db.add(instance)
            await db.commit()
            await db.refresh(instance)
        return instance

    async def assign_asset(self, db: AsyncSession, slot: str, asset_id: int | None) -> BrandingSlotZuweisung:
        instance = await self._get_or_create(db, slot)
        if asset_id is not None:
            asset_result = await db.execute(select(BrandingAsset).where(BrandingAsset.id == asset_id))
            if asset_result.scalar_one_or_none() is None:
                raise HTTPException(status_code=404, detail="Asset nicht gefunden.")
        instance.asset_id = asset_id
        await db.commit()
        await db.refresh(instance)
        return instance

    async def update_link(self, db: AsyncSession, slot: str, link: str | None) -> BrandingSlotZuweisung:
        if not BRANDING_SLOTS[slot]["verlinkbar"]:
            raise HTTPException(status_code=400, detail="Für diesen Slot kann kein Link gesetzt werden.")
        instance = await self._get_or_create(db, slot)
        instance.link = link
        await db.commit()
        await db.refresh(instance)
        return instance

    async def reset_all(self, db: AsyncSession) -> None:
        result = await db.execute(select(BrandingSlotZuweisung))
        for instance in result.scalars().all():
            instance.asset_id = None
            instance.link = BRANDING_SLOTS.get(instance.slot, {}).get("standard_link")
        await db.commit()


class CRUDLogoListeEintrag:
    def _check_bereich(self, bereich: str) -> None:
        if bereich not in LOGO_LISTEN_BEREICHE:
            raise HTTPException(status_code=404, detail="Unbekannter Logo-Listen-Bereich.")

    async def get_all(self, db: AsyncSession, bereich: str) -> list[LogoListeEintrag]:
        self._check_bereich(bereich)
        result = await db.execute(
            select(LogoListeEintrag)
            .where(LogoListeEintrag.bereich == bereich)
            .order_by(LogoListeEintrag.reihenfolge)
        )
        return list(result.scalars().all())

    async def create(
        self, db: AsyncSession, bereich: str, obj_in: LogoListeEintragCreate
    ) -> LogoListeEintrag:
        self._check_bereich(bereich)
        asset_result = await db.execute(select(BrandingAsset).where(BrandingAsset.id == obj_in.asset_id))
        if asset_result.scalar_one_or_none() is None:
            raise HTTPException(status_code=404, detail="Asset nicht gefunden.")

        max_result = await db.execute(
            select(func.max(LogoListeEintrag.reihenfolge)).where(LogoListeEintrag.bereich == bereich)
        )
        max_reihenfolge = max_result.scalar_one_or_none()
        next_reihenfolge = (max_reihenfolge + 1) if max_reihenfolge is not None else 0

        instance = LogoListeEintrag(
            bereich=bereich, asset_id=obj_in.asset_id, link=obj_in.link, reihenfolge=next_reihenfolge
        )
        db.add(instance)
        await db.commit()
        await db.refresh(instance)
        return instance

    async def update(
        self, db: AsyncSession, bereich: str, eintrag_id: int, obj_in: LogoListeEintragUpdate
    ) -> LogoListeEintrag:
        self._check_bereich(bereich)
        result = await db.execute(
            select(LogoListeEintrag).where(
                LogoListeEintrag.id == eintrag_id, LogoListeEintrag.bereich == bereich
            )
        )
        instance = result.scalar_one_or_none()
        if instance is None:
            raise HTTPException(status_code=404, detail="Logo-Listeneintrag nicht gefunden.")
        instance.link = obj_in.link
        await db.commit()
        await db.refresh(instance)
        return instance

    async def delete(self, db: AsyncSession, bereich: str, eintrag_id: int) -> None:
        self._check_bereich(bereich)
        result = await db.execute(
            select(LogoListeEintrag).where(
                LogoListeEintrag.id == eintrag_id, LogoListeEintrag.bereich == bereich
            )
        )
        instance = result.scalar_one_or_none()
        if instance is None:
            return
        await db.delete(instance)
        await db.commit()

    async def reorder(
        self, db: AsyncSession, bereich: str, obj_in: LogoListeReorderUpdate
    ) -> list[LogoListeEintrag]:
        self._check_bereich(bereich)
        ids = [item.id for item in obj_in.reihenfolge]
        result = await db.execute(
            select(LogoListeEintrag).where(
                LogoListeEintrag.id.in_(ids), LogoListeEintrag.bereich == bereich
            )
        )
        instances_by_id = {i.id: i for i in result.scalars().all()}
        for item in obj_in.reihenfolge:
            instance = instances_by_id.get(item.id)
            if instance is not None:
                instance.reihenfolge = item.reihenfolge
        await db.commit()
        return await self.get_all(db, bereich)

    async def reset_all(self, db: AsyncSession) -> None:
        result = await db.execute(select(LogoListeEintrag))
        for instance in result.scalars().all():
            await db.delete(instance)
        await db.commit()


crud_branding_asset = CRUDBrandingAsset()
crud_branding_slot_zuweisung = CRUDBrandingSlotZuweisung()
crud_logo_liste_eintrag = CRUDLogoListeEintrag()
