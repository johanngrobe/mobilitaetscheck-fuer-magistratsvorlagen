# Deployment mit Docker Compose

Diese Anleitung beschreibt, wie du das Projekt mit **Docker Compose** deployen kannst.  
Im Repository befinden sich zwei Vorlagendateien:

- `docker-compose.yml.example`
- `example.env`

Beide müssen kopiert und angepasst werden, bevor das Deployment erfolgt.

---

## 1. Voraussetzungen

Du benötigst:

- **Docker**
- **Docker Compose** (bzw. `docker compose`)

---

## 2. Konfigurationsdateien vorbereiten

### 2.1 `.env` Datei erstellen

Kopiere die Beispiel-Datei:

```bash
cp example.env .env
```

Passe anschließend alle Werte an deine Umgebung an.  
⚠️ **Wichtig:** Die `.env` darf nicht ins Git-Repository committed werden.

---

### 2.2 `docker-compose.yml` erstellen

```bash
cp docker-compose.yml.example docker-compose.yml
```

Je nach Infrastruktur können nun Ports, Volumes und Umgebungsvariablen angepasst werden.

---

## 3. Docker Compose Beispiel

Die folgende Einbindung erfolgt automatisch über das  
**mkdocs-include-markdown-plugin**:

```yaml
--8<-- "docker-compose.yml.example"
```

---

## 4. Container starten

Starte alle Dienste im Hintergrund:

```bash
docker compose up -d
```

Logs ansehen:

```bash
docker compose logs -f
```

---

## 5. Zugriff auf die Applikation

Der FastAPI-Server läuft standardmäßig auf:

```
http://localhost:8000
```

Dort ist das Frontend erreichbar.

Falls der Port über Docker gemappt wurde (z. B. `8000:8000`), erreichst du ihn extern ebenfalls unter Port **8000**.

Die FastAPI-Dokumentation erreichst du unter:

- Swagger UI: `http://localhost:8000/api/v1/docs`
- ReDoc: `http://localhost:8000/api/v1/redoc`

---

## 6. Container stoppen

```bash
docker compose down
```

Mit Volumes löschen:

```bash
docker compose down -v
```

---

## 7. Deployment aktualisieren

Neue Version deployen:

1. Repository aktualisieren:

   ```bash
   git pull
   ```

2. Neue Images ziehen (falls verwendet):

   ```bash
   docker compose pull
   ```

3. Neustarten:

   ```bash
   docker compose up -d
   ```
