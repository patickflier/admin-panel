FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install uv
RUN pip install uv

# Copy project files
COPY pyproject.toml uv.lock* /app/
# Install runtime dependencies via uv (adds to lock, installs .venv)
RUN uv sync --no-dev

# Copy the rest of your project
COPY . /app

# Final command: migrate then start
CMD ["sh", "-c", "uv run alembic upgrade head && uv run uvicorn app.main:app --host 0.0.0.0 --port 8000"]
