FROM python:3.12-slim

WORKDIR /app

RUN pip install uv

COPY pyproject.toml .
RUN uv venv
RUN uv pip install -e .

COPY . .

EXPOSE 8000