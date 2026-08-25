from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.plattform_einstellung import PlattformEinstellung
from app.schemas.plattform_einstellung import PlattformEinstellungUpdate

SINGLETON_ID = 1


class CRUDPlattformEinstellung:
    async def get(self, db: AsyncSession) -> PlattformEinstellung:
        result = await db.execute(
            select(PlattformEinstellung).where(PlattformEinstellung.id == SINGLETON_ID)
        )
        instance = result.scalar_one_or_none()
        if instance is None:
            instance = PlattformEinstellung(id=SINGLETON_ID)
            db.add(instance)
            await db.commit()
            await db.refresh(instance)
        return instance

    async def update(
        self, db: AsyncSession, obj_in: PlattformEinstellungUpdate
    ) -> PlattformEinstellung:
        instance = await self.get(db)
        for field, value in obj_in.model_dump(exclude_unset=True).items():
            setattr(instance, field, value)
        await db.commit()
        await db.refresh(instance)
        return instance


crud_plattform_einstellung = CRUDPlattformEinstellung()
