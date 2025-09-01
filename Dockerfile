FROM python:3.12-slim as builder

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev libpq-dev pkg-config && \
    rm -rf /var/lib/apt/lists/*

COPY requirements/dev.ini .
RUN pip install --user --no-cache-dir -r dev.ini

FROM python:3.12-slim as production

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends curl libpq5 && \
    rm -rf /var/lib/apt/lists/*

RUN groupadd -r app && useradd -r -g app app

COPY --from=builder /root/.local /home/app/.local
COPY --chown=app:app . .

USER app

ENV PATH="/home/app/.local/bin:${PATH}"
ENV PYTHONPATH=/app

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]