# Übersicht der Umgebungsvariablen

Diese Seite beschreibt alle verfügbaren Umgebungsvariablen, die für den Betrieb der Anwendung erforderlich sind.  
Sie können in einer `.env` Datei oder über das Deployment-System gesetzt werden.

---

## 🌐 Allgemeine Einstellungen

| Variable        | Beschreibung                                   | Standard/Beispiel         |
| --------------- | ---------------------------------------------- | ------------------------- |
| `DOMAIN`        | Domain, unter der das Backend erreichbar ist   | `"localhost"`             |
| `FRONTEND_HOST` | URL des Frontends (für CORS, Redirects etc.)   | `"http://localhost:5173"` |
| `ENVIRONMENT`   | Betriebsmodus (`development`, `production`, …) | `"production"`            |

---

## 🖼️ Branding & Uploads

| Variable              | Beschreibung                                                                                   | Standard/Beispiel      |
| ---------------------- | ----------------------------------------------------------------------------------------------- | ----------------------- |
| `BRANDING_UPLOAD_DIR`  | Verzeichnis für hochgeladene Branding-Bilder (Logos, Favicon). Relativ zum Backend-Arbeitsverzeichnis oder absolut. Wird beim Start automatisch angelegt. | `"./uploads/branding"` |

---

## 🗄️ Datenbank-Einstellungen

| Variable            | Beschreibung                            | Beispiel               |
| ------------------- | --------------------------------------- | ---------------------- |
| `POSTGRES_SERVER`   | Hostname oder IP des PostgreSQL-Servers | `"localhost"`          |
| `POSTGRES_PORT`     | Port des PostgreSQL-Servers             | `5432`                 |
| `POSTGRES_DB`       | Name der Datenbank                      | `"mobilitaetscheckdb"` |
| `POSTGRES_USER`     | Datenbank-Benutzername                  | `"mobilitaetscheck"`   |
| `POSTGRES_PASSWORD` | Passwort des DB-Benutzers               | `"DB_PASSWORD"`        |

---

## 🔐 Authentifizierung & Tokens

| Variable                      | Beschreibung                          | Beispiel          |
| ----------------------------- | ------------------------------------- | ----------------- |
| `JWT_SECRET_KEY`              | Secret zum Signieren von JWTs         | `"JWT_SECRET"`    |
| `RESET_PASSWORD_TOKEN_SECRET` | Secret für Passwort-Reset-Token       | `"RESET_SECRET"`  |
| `VERIFICATION_TOKEN_SECRET`   | Secret für Verifizierungs-Token       | `"VERIFY_SECRET"` |
| `JWT_LIFETIME_SECONDS`        | Gültigkeitsdauer der JWTs in Sekunden | `43200`           |

---

## ✉️ E-Mail Einstellungen

| Variable          | Beschreibung                              | Beispiel                                    |
| ----------------- | ----------------------------------------- | ------------------------------------------- |
| `MAIL_USERNAME`   | SMTP Benutzername                         | `username`                                  |
| `MAIL_PASSWORD`   | SMTP Passwort                             | `password`                                  |
| `MAIL_FROM`       | Absenderadresse                           | `"mail@example.com"`                        |
| `MAIL_FROM_NAME`  | Name des Absenders                        | `"Mobilitaetscheck für Magistratsvorlagen"` |
| `MAIL_PORT`       | SMTP Port                                 | `587`                                       |
| `MAIL_SERVER`     | SMTP Host                                 | `"mail.example.com"`                        |
| `MAIL_STARTTLS`   | STARTTLS aktivieren (`True/False`)        | `True`                                      |
| `MAIL_SSL_TLS`    | SSL/TLS verwenden (`True/False`)          | `False`                                     |
| `USE_CREDENTIALS` | SMTP-Anmeldung aktivieren (`True/False`)  | `True`                                      |
| `VALIDATE_CERTS`  | SSL-Zertifikate validieren (`True/False`) | `True`                                      |

---
