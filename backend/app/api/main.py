from fastapi import APIRouter

from app.core.deps import auth_backend, fastapi_users
from app.core.config import settings
from app.api.routers import (
    bool_erweitert,
    gemeinde_gebiet,
    indikator,
    klimacheck,
    klimarelevanzpruefung_eingabe,
    klimarelevanzpruefung_eingabe_fb1,
    klimarelevanzpruefung_eingabe_fb2,
    klimarelevanzpruefung_eingabe_fb3,
    klimarelevanzpruefung_eingabe_fb4,
    klimarelevanzpruefung_vorhaben,
    klimarelevanzpruefung_energiestandard,
    magistratsvorlage,
    mobilitaetscheck_eingabe,
    mobilitaetscheck_eingabe_ziel_ober,
    mobilitaetscheck_eingabe_ziel_unter,
    mobilitaetscheck_ziel_ober,
    mobilitaetscheck_ziel_unter,
    option,
    tag,
    textblock,
    user,
    public,
)
from app.schemas.user import UserRead, UserCreate, UserUpdate

router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth", tags=["Auth"]
)
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)
router.include_router(
    fastapi_users.get_reset_password_router(), prefix="/auth", tags=["Auth"]
)
router.include_router(
    fastapi_users.get_verify_router(UserRead), prefix="/auth", tags=["Auth"]
)
router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["Users"],
)
router.include_router(
    user.router,
    prefix="/users",
    tags=["Users"],
)
router.include_router(public.router, prefix="/public", tags=["Public"])
router.include_router(
    magistratsvorlage.router,
    prefix="/magistratsvorlage",
    tags=["Magistratsvorlage"],
)
router.include_router(
    mobilitaetscheck_eingabe.router,
    prefix="/mobilitaetscheck/eingabe",
    tags=["Mobilitätscheck", "Eingabe"],
)
router.include_router(
    klimacheck.router,
    prefix="/klimacheck/eingabe",
    tags=["Klimacheck", "Eingabe"],
)
router.include_router(
    klimarelevanzpruefung_eingabe.router,
    prefix="/klimarelevanzpruefung/eingabe",
    tags=["Klimarelevanzprüfung", "Eingabe"],
)
router.include_router(
    klimarelevanzpruefung_eingabe_fb1.router,
    prefix="/klimarelevanzpruefung/eingabe/fb1",
    tags=["Klimarelevanzprüfung", "Eingabe"],
)
router.include_router(
    klimarelevanzpruefung_eingabe_fb2.router,
    prefix="/klimarelevanzpruefung/eingabe/fb2",
    tags=["Klimarelevanzprüfung", "Eingabe"],
)
router.include_router(
    klimarelevanzpruefung_eingabe_fb3.router,
    prefix="/klimarelevanzpruefung/eingabe/fb3",
    tags=["Klimarelevanzprüfung", "Eingabe"],
)
router.include_router(
    klimarelevanzpruefung_eingabe_fb4.router,
    prefix="/klimarelevanzpruefung/eingabe/fb4",
    tags=["Klimarelevanzprüfung", "Eingabe"],
)
router.include_router(
    klimarelevanzpruefung_energiestandard.router,
    prefix="/klimarelevanzpruefung/energiestandard",
    tags=["Klimarelevanzprüfung"],
)
router.include_router(
    klimarelevanzpruefung_vorhaben.router,
    prefix="/klimarelevanzpruefung/vorhaben",
    tags=["Klimarelevanzprüfung"],
)
router.include_router(
    mobilitaetscheck_eingabe_ziel_ober.router,
    prefix="/mobilitaetscheck/eingabe/ziel/ober",
    tags=["Mobilitätscheck", "Eingabe"],
)
router.include_router(
    mobilitaetscheck_eingabe_ziel_unter.router,
    prefix="/mobilitaetscheck/eingabe/ziel/unter",
    tags=["Mobilitätscheck", "Eingabe"],
)
router.include_router(
    gemeinde_gebiet.router,
    prefix="/einstellungen/gebiet",
    tags=["Einstellungen", "Gebiet"],
)
router.include_router(
    indikator.router,
    prefix="/einstellungen/indikator",
    tags=["Einstellungen", "Indikator"],
)
router.include_router(
    textblock.router,
    prefix="/einstellungen/textblock",
    tags=["Einstellungen", "Textblock"],
)
router.include_router(
    tag.router, prefix="/einstellungen/tag", tags=["Einestellungen", "Tag"]
)
router.include_router(
    mobilitaetscheck_ziel_ober.router,
    prefix="/einstellungen/mobilitaetscheck/ziel/ober",
    tags=["Einstellungen", "Mobilitätscheck"],
)
router.include_router(
    mobilitaetscheck_ziel_unter.router,
    prefix="/einstellungen/mobilitaetscheck/ziel/unter",
    tags=["Einstellungen", "Mobilitätscheck"],
)
router.include_router(
    bool_erweitert.router,
    prefix="/einstellungen/bool-erweitert",
    tags=["Einstellungen", "Boolean Erweitert"],
)
router.include_router(option.router, prefix="/option", tags=["Option"])
