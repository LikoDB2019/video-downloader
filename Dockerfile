# Używamy lekkiej wersji Pythona
FROM python:3.9-slim

# Instalujemy FFmpeg (kluczowe dla 1080p!)
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# Ustawiamy katalog roboczy
WORKDIR /app

# Kopiujemy pliki
COPY . /app

# Instalujemy biblioteki
RUN pip install --no-cache-dir -r requirements.txt

# Tworzymy folder na pobieranie
RUN mkdir -p downloads

# Otwieramy port (Render wymaga 8000 lub podobnego, Flask domyślnie 5000)
ENV PORT=5000
EXPOSE 5000

# Komenda uruchamiająca (Gunicorn jest szybszy niż zwykły python app.py)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--timeout", "120", "app:app"]