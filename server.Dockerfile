FROM python:3.10-slim-bullseye

EXPOSE 8222

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

COPY ./server/requirements.txt .
RUN pip install --upgrade pip
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY ./server/src/ /app/src

RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

ENV PYTHONPATH /app/src

CMD ["gunicorn", "--bind", "0.0.0.0:8222", "-k", "uvicorn.workers.UvicornWorker", "src.main:app"]
