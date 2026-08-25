BRANDING_SLOTS = {
    "favicon": {
        "label": "Favicon",
        "beschreibung": "Wird als Browser-Tab-Icon verwendet.",
        "bereich": "Browser",
        "erlaubte_typen": ["image/x-icon", "image/png", "image/svg+xml"],
    },
    "menue-logo": {
        "label": "Logo in der Menüleiste",
        "beschreibung": "Wird oben links in der Navigationsleiste angezeigt.",
        "bereich": "Menüleiste",
        "erlaubte_typen": ["image/png", "image/svg+xml", "image/webp"],
    },
}

for _slot in BRANDING_SLOTS.values():
    _slot.setdefault("verlinkbar", False)
    _slot.setdefault("standard_link", None)

LOGO_LISTEN_BEREICHE = {
    "footer": {
        "label": "Footer-Logos",
        "beschreibung": "Beliebig viele Logos im Footer anzeigen.",
    },
    "login": {
        "label": "Login- und Registrierungs-Logos",
        "beschreibung": "Beliebig viele Logos auf der Anmelde- und Registrierungsseite anzeigen.",
    },
}

MAX_UPLOAD_SIZE_BYTES = 2 * 1024 * 1024  # 2 MB

ALLOWED_UPLOAD_TYPES = {
    "image/x-icon",
    "image/vnd.microsoft.icon",
    "image/png",
    "image/svg+xml",
    "image/webp",
    "image/jpeg",
}

CONTENT_TYPE_TO_EXTENSION = {
    "image/x-icon": "ico",
    "image/vnd.microsoft.icon": "ico",
    "image/png": "png",
    "image/svg+xml": "svg",
    "image/webp": "webp",
    "image/jpeg": "jpg",
}
