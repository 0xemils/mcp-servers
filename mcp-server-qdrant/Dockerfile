# Builder stage
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

WORKDIR /app

ENV UV_LINK_MODE=copy
ENV UV_COMPILE_BYTECODE=1

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev --no-editable

# Install project sources
ADD . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --no-editable

# Dev stage
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS dev

WORKDIR /app

ENV UV_LINK_MODE=copy
ENV UV_COMPILE_BYTECODE=1

# Copy the virtual environment from the builder stage
COPY --from=builder /app/.venv /app/.venv

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --group dev --group debug

ENV PATH="/app/.venv/bin:$PATH"

CMD ["tail", "-f", "/dev/null"]

# Production stage
FROM python:3.12-slim-bookworm AS prod

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8002

CMD ["python", "-m", "mcp_server_qdrant", "--host", "0.0.0.0", "--port", "8002"]