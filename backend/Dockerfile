FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Instala netcat para esperar la DB
RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*


EXPOSE 5000

# Espera a que MySQL esté listo antes de arrancar Flask
CMD ["python", "app.py"]

