# Bare-Metal Installation

Diese Anleitung beschreibt, wie das Projekt **ohne Docker**, also direkt auf einem Linux‑Server installiert und betrieben werden kann.

---

## 1. Voraussetzungen

### Softwareanforderungen

Auf dem Server müssen folgende Pakete installiert sein:

- **Node.js 20** (für das Frontend)
- **uv** (Python Package Manager von Astral)
- **Postgresql 17**

---

## 1. Abhängigkeiten installieren

```bash
apt install -y \
  build-essential \
  git \
  curl \
  python3-dev
```

## 2. Notwendige Tools installieren

Es werden folgende Tools benötigt. Diese sind aus den offiziellen Quellen zu installieren :

- uv (Python) → https://docs.astral.sh/uv/
- Node.js 22 → https://nodejs.org/en/download
- PostgreSQL 17 → https://www.postgresql.org/download/

## 2. Repository klonen

```bash
git clone https://github.com/ritmo-hsrm/mobilitaetscheck-fuer-magistratsvorlagen
```

---

## 3. Umgebungsvariablen konfigurieren

Erstelle eine `.env` Datei:

```bash
cp env.example .env
```

Setze `HOST_URL` auf die öffentlich erreichbare URL des Backends (z.B.
`https://mobilitaetscheck.example.com`). Diese wird u.a. für Links in E-Mails sowie für die URLs
hochgeladener Branding-Bilder (Logos, Favicon) verwendet – bleibt sie auf dem Standardwert
`http://localhost:8000`, funktionieren diese Links außerhalb des Servers nicht.

Über `BRANDING_UPLOAD_DIR` lässt sich der Speicherort für hochgeladene Branding-Bilder (Logos,
Favicon) konfigurieren. Standardmäßig liegt er innerhalb des Backend-Verzeichnisses; bei Bedarf
kann ein anderer (auch absoluter) Pfad gesetzt werden. Das Verzeichnis wird beim Start automatisch
angelegt, muss aber für den Benutzer beschreibbar sein, unter dem der Backend-Dienst läuft.

---

## 4. Frontend installieren und builden

Das Frontend basiert auf **Vite** und muss lokal gebaut werden.

```bash
cd frontend
npm ci
npm run build
```

Der Produktionsbuild befindet sich anschließend im Ordner:

```
frontend/dist/
```

Dieser Build wird später vom Backend ausgeliefert.

---

## 5. Backend installieren

Das Backend basiert auf **FastAPI** und verwendet **uv** zur Paketverwaltung.

```bash
cd /pfad/zum/root/ordner
uv sync --no-dev
```

Passe alle Variablen wie Domain, Datenbank‑Zugangsdaten und SMTP an deine Umgebung an.

## 6. Datenbank einrichten

Richte ein Postgresql-Datenbank gemäß der `.env` Datei ein. Nachfolgend sind die grundlegenden Befehle zur Einrichtung der Datenbank beschrieben.

```bash
sudo -u postgres createuser -P mobilitaetscheck
sudo -u postgres createdb -O mobilitaetscheck mobilitaetscheck
```

Prüfe, ob die PostgreSQL Enconding UTF-8 sind.

```bash
sudo -u postgres psql -c "SHOW client_encoding;"
sudo -u postgres psql -c "SHOW server_encoding;"
```

Falls einer der Werte SQL_ASCII ist, setze die Werte explizit auf UTF-8.

```bash
sudo -u postgres psql -c "ALTER ROLE mobilitaetscheck SET client_encoding = 'UTF8';"
sudo -u postgres psql -c "ALTER DATABASE mobilitaetscheck SET client_encoding = 'UTF8';"
```

---

## 7. Backend starten

Das Backend kann über uvicorn gestartet werden.

```bash
source .venv/bin/activate
cd pfad/zum/backend
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

## 9. Optional: systemd-Service einrichten (für Produktion)

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
EnvironmentFile=/pfad/zur/root/.env
ExecStart=/pfad/zum/backend/.venv/bin/fastapi run app/main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Service aktivieren:

```bash
systemctl daemon-reload
systemctl enable mobilitaetscheck
systemctl start mobilitaetscheck
```

---

# Bare-Metal Update

## 1. Service stoppen

```bash
systemctl stop mobilitaetscheck
```

## 2. Repo aktualisieren

```bash
cd /pfad/zum/repo
git pull
```

## 3. Frontend aktualisieren

```bash
cd frontend
npm ci
npm run build
```

## 4. Backend aktualisieren

```bash
source ./.venv/bin/activate
cd /pfad/zum/backend
uv sync --no-dev
```

## 5. Datenbank migrieren

```bash
cd /pfad/zum/backend
source ./.venv/bin/activate
alembic upgrade head
```

## 6. Service starten

```bash
systemctl start mobilitaetscheck
```
