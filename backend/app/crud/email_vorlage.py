from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.email_vorlage import EmailVorlage
from app.schemas.email_vorlage import EmailVorlageUpdate
from app.services.mail.vorlagen_registry import DEFAULT_VORLAGEN, get_default_inhalt


class CRUDEmailVorlage:
    async def get_all(self, db: AsyncSession) -> list[EmailVorlage]:
        result = await db.execute(select(EmailVorlage))
        by_key = {v.key: v for v in result.scalars().all()}
        return [by_key.get(key) or EmailVorlage(key=key) for key in DEFAULT_VORLAGEN]

    async def get_by_key(self, db: AsyncSession, key: str) -> EmailVorlage:
        if key not in DEFAULT_VORLAGEN:
            raise ValueError(f"Unbekannte Email-Vorlage: {key}")
        result = await db.execute(select(EmailVorlage).where(EmailVorlage.key == key))
        instance = result.scalar_one_or_none()
        return instance or EmailVorlage(key=key)

    async def update(
        self, db: AsyncSession, key: str, obj_in: EmailVorlageUpdate
    ) -> EmailVorlage:
        if key not in DEFAULT_VORLAGEN:
            raise ValueError(f"Unbekannte Email-Vorlage: {key}")
        result = await db.execute(select(EmailVorlage).where(EmailVorlage.key == key))
        instance = result.scalar_one_or_none()
        if instance is None:
            instance = EmailVorlage(key=key)
            db.add(instance)
        for field, value in obj_in.model_dump(exclude_unset=True).items():
            setattr(instance, field, value)
        await db.commit()
        await db.refresh(instance)
        return instance

    async def reset(self, db: AsyncSession, key: str) -> EmailVorlage:
        if key not in DEFAULT_VORLAGEN:
            raise ValueError(f"Unbekannte Email-Vorlage: {key}")
        result = await db.execute(select(EmailVorlage).where(EmailVorlage.key == key))
        instance = result.scalar_one_or_none()
        if instance is not None:
            await db.delete(instance)
            await db.commit()
        return EmailVorlage(key=key)

    async def get_resolved(self, db: AsyncSession, key: str) -> tuple[str, str]:
        """Return (betreff, inhalt) - the admin override if present, else the default."""
        instance = await self.get_by_key(db, key)
        default = DEFAULT_VORLAGEN[key]
        betreff = instance.betreff or default["betreff"]
        inhalt = instance.inhalt or get_default_inhalt(key)
        return betreff, inhalt


crud_email_vorlage = CRUDEmailVorlage()
