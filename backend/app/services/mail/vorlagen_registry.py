from pathlib import Path

TEMPLATE_FOLDER = Path(__file__).parent / "templates"

DEFAULT_VORLAGEN = {
    "account-bestaetigen": {
        "betreff": "Willkommen – bitte bestätigen Sie Ihren Account",
        "datei": "account-bestaetigen.html",
        "platzhalter": ["vorname", "nachname", "rolle", "gemeinde", "url"],
    },
    "einladung": {
        "betreff": "Einladung zur Registrierung beim Mobilitätscheck für Magistratsvorlagen",
        "datei": "einladung.html",
        "platzhalter": ["rolle", "gemeinde", "url", "gueltigkeitsdauer"],
    },
    "passwort-zuruecksetzen": {
        "betreff": "Passwort zurücksetzen",
        "datei": "passwort-zuruecksetzen.html",
        "platzhalter": ["vorname", "nachname", "url"],
    },
}


def get_default_inhalt(key: str) -> str:
    datei = DEFAULT_VORLAGEN[key]["datei"]
    return (TEMPLATE_FOLDER / datei).read_text(encoding="utf-8")
