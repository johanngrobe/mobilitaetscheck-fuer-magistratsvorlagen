from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_async_session
from app.crud.exceptions import NotFoundError
from app.crud.user import crud_user as crud

router = APIRouter()


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
