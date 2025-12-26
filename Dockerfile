# Wykorzystaj obraz z Pythonem
FROM python:3.10-slim

# Zainstaluj ffmpeg (kluczowe dla video downloadera!)
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

# Komenda startowa
CMD ["gunicorn", "app:app"]