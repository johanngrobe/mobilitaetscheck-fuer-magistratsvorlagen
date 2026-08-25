from jinja2 import Template
from fastapi_mail import MessageSchema, MessageType

from app.core.config import settings
from app.core.db import async_session_maker
from app.crud.email_vorlage import crud_email_vorlage
from app.models.user import User
from app.services.mail.config_mail import Mail
from app.utils.url_util import add_query_params


async def _render_vorlage(key: str, context: dict) -> tuple[str, str]:
    """Resolve the admin-editable (or default) subject/body for a template key and render placeholders."""
    async with async_session_maker() as db:
        betreff, inhalt = await crud_email_vorlage.get_resolved(db, key)
    return Template(betreff).render(**context), Template(inhalt).render(**context)


async def send_verification(user: User, token: str):
    url = add_query_params(
        f"{settings.HOST_URL}/auth/account-bestaetigen", {"token": token}
    )

    context = {
        "vorname": user.vorname,
        "nachname": user.nachname,
        "rolle": user.rolle.name,
        "gemeinde": user.gemeinde.name,
        "url": url,
    }

    try:
        subject, body = await _render_vorlage("account-bestaetigen", context)
        message = MessageSchema(
            subject=subject,
            recipients=[user.email],
            body=body,
            subtype=MessageType.html,
        )
        await Mail.send_message(message)
    except Exception as e:
        print(f"Error sending verification email: {e}")


def _format_gueltigkeitsdauer(hours: int) -> str:
    if hours == 1:
        return "1 Stunde"
    if hours < 24:
        return f"{hours} Stunden"
    days = hours // 24
    if days == 1:
        return "1 Tag"
    return f"{days} Tage"


async def send_einladung(
    email: str, gemeinde_name: str, rolle_name: str, token: str, valid_hours: int
):
    url = add_query_params(
        f"{settings.HOST_URL}/auth/registrieren/einladung", {"token": token}
    )

    context = {
        "rolle": rolle_name,
        "gemeinde": gemeinde_name,
        "url": url,
        "gueltigkeitsdauer": _format_gueltigkeitsdauer(valid_hours),
    }

    try:
        subject, body = await _render_vorlage("einladung", context)
        message = MessageSchema(
            subject=subject,
            recipients=[email],
            body=body,
            subtype=MessageType.html,
        )
        await Mail.send_message(message)
    except Exception as e:
        print(f"Error sending invite email: {e}")


async def send_reset_password(user: User, token: str):

    url = add_query_params(
        f"{settings.HOST_URL}/auth/passwort-zuruecksetzen", {"token": token}
    )

    context = {
        "vorname": user.vorname,
        "nachname": user.nachname,
        "rolle": user.rolle.name,
        "url": url,
    }

    try:
        subject, body = await _render_vorlage("passwort-zuruecksetzen", context)
        message = MessageSchema(
            subject=subject,
            recipients=[user.email],
            body=body,
            subtype=MessageType.html,
        )
        await Mail.send_message(message)
    except Exception as e:
        print(f"Error sending reset password email: {e}")
