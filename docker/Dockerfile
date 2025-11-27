# =============================================
# 1) FRONTEND BUILD (Vite)
# =============================================
FROM node:20 AS frontend-build

WORKDIR /frontend

COPY ../frontend/package*.json ./
RUN npm install

COPY ../frontend .
RUN npm run build


# =============================================
# 2) BACKEND (FastAPI + uv)
# =============================================
FROM ghcr.io/astral-sh/uv:python3.13-trixie-slim AS backend

ENV UV_SYSTEM_PYTHON=1

WORKDIR /app

# Backend dependencies
COPY ../backend/pyproject.toml ../backend/uv.lock ./
RUN uv sync --no-dev

# Backend source
COPY ../backend .

# SPA
COPY --from=frontend-build /frontend/dist ./app/frontend_dist

ENV FRONTEND_DIR="app/frontend_dist"

# Entrypoint
COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Make uv venv globally usable
ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]
