FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py init_db.py ./

RUN mkdir -p /app/data \
    && useradd --create-home --uid 10001 c3user \
    && chown -R c3user:c3user /app

USER c3user

EXPOSE 5003

CMD ["sh", "-c", "python init_db.py && gunicorn --workers 2 --bind 0.0.0.0:5003 app:app"]
