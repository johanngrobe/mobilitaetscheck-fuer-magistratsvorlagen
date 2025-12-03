# Bare-Metal Installation

Diese Anleitung beschreibt, wie das Projekt **ohne Docker**, also direkt auf einem Linux‑Server installiert und betrieben werden kann.

---

# 1. Voraussetzungen

## Softwareanforderungen

Auf dem Server müssen folgende Pakete installiert sein:

- **Node.js 20** (für das Frontend)
- **uv** (Python Package Manager von Astral)
- **Postgresql 17**

---

# 2. Repository klonen

```bash
git clone https://github.com/johanngrobe/mobilitaetscheck-fuer-magistratsvorlagen
```

---

# 3. Frontend installieren und builden

Das Frontend basiert auf **Vite** und muss lokal gebaut werden.

```bash
cd frontend
npm install
npm run build
```

Der Produktionsbuild befindet sich anschließend im Ordner:

```
frontend/dist/
```

Dieser Build wird später vom Backend ausgeliefert.

---

# 4. Backend installieren

Das Backend basiert auf **FastAPI** und verwendet **uv** zur Paketverwaltung.

```bash
cd ../backend
uv sync --no-dev
```

---

# 5. Umgebungsvariablen konfigurieren

Erstelle eine `.env` Datei:

```bash
cp example.env .env
```

Passe alle Variablen wie Domain, Datenbank‑Zugangsdaten und SMTP an deine Umgebung an.

# 6. Datenbank einrichten

Richte ein Postgresql-Datenbank gemäß der `.env` Datei ein.

---

# 7. Backend starten

Das Backend kann über uvicorn gestartet werden.

```bash
source .venv/bin/activate
fastapi run app/main.py
```

Der Server ist erreichbar unter:

```
http://localhost:8000
```

API Docs:

- Swagger: `http://localhost:8000/api/v1/docs`
- ReDoc: `http://localhost:8000/api/v1/redoc`

---

# 9. Optional: systemd-Service einrichten (für Produktion)

Datei erstellen:

```bash
sudo nano /etc/systemd/system/mobilitaetscheck.service
```

Inhalt:

```ini
[Unit]
Description=Mobilitaetscheck
After=network.target

[Service]
WorkingDirectory=/pfad/zum/backend
EnvironmentFile=/pfad/zum/backend/.env
ExecStart=/pfad/zum/backend/.venv/bin/fastapi run app/main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Service aktivieren:

```bash
sudo systemctl daemon-reload
sudo systemctl enable mobilitaetscheck
sudo systemctl start mobilitaetscheck
```
