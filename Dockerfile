# Dockerfile
FROM python:3.12-slim

# dont write .pyc files, disable output buffering
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN useradd -m -u 10001 botuser

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN python -m pip install --no-cache-dir -r /app/requirements.txt

COPY bot.py /app/bot.py

RUN mkdir -p /data && chown -R botuser:botuser /data

USER botuser

CMD ["python", "/app/bot.py"]
