FROM python:3.11-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

COPY src/ ./src/
COPY configs/ ./configs/

EXPOSE 8000
CMD ["uv", "run", "uvicorn", "src.serve.api:app", "--host", "0.0.0.0", "--port", "8000"]
