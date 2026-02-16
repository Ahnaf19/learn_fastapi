# ============================================================
# Dockerfile — app/ (Demo API: Users & Orders)
# ============================================================
# Build: docker build -t demo-api .
# Run:   docker run -p 8000:8000 demo-api
# ============================================================

# Use the official uv image — includes Python 3.10 + uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.10-bookworm-slim

WORKDIR /app

# ── Layer caching optimisation ────────────────────────────
# Copy dependency files first. Docker only re-runs the install
# step when pyproject.toml or uv.lock actually change.
COPY pyproject.toml uv.lock ./

# Install production dependencies only (no pytest/httpx)
# --frozen       → use exact versions from uv.lock (no resolution)
# --no-dev       → skip [dependency-groups] dev deps
# --no-install-project → don't install the project itself as a package
RUN uv sync --frozen --no-dev --no-install-project

# ── Application code ─────────────────────────────────────
COPY app/ ./app/

# Put the venv's bin on PATH so we can call uvicorn directly
ENV PATH="/app/.venv/bin:$PATH"

# ── Runtime ──────────────────────────────────────────────
EXPOSE 8000

# --host 0.0.0.0 → listen on all interfaces (required inside Docker)
# --port 8000    → explicit, matches EXPOSE above
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
