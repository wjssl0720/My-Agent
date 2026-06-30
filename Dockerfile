FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml README.md ./
COPY src ./src
COPY configs ./configs
COPY verification ./verification
RUN pip install --no-cache-dir -e ".[dev]"
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
