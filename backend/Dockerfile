# Użyj obrazu Pythona jako bazowego
FROM python:3.9-slim

# Ustawienie katalogu roboczego w kontenerze
WORKDIR /app

# Skopiuj plik requirements.txt i zainstaluj zależności
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Skopiuj cały kod aplikacji do kontenera
COPY . /app/

# Skopiuj plik .env do kontenera
COPY .env /app/.env

# Zainstaluj zależność dotenv dla Pythona (jeśli jeszcze jej nie zainstalowano)
RUN pip install python-dotenv

# Ustawienie zmiennych środowiskowych z pliku .env
# Plik .env jest parsowany w momencie działania aplikacji, np. przez bibliotekę `python-dotenv`

# Uruchom aplikację
CMD ["python", "assist_b.py"]
