FROM python:3.9-slim

WORKDIR /app

# Dependenciesni o'rnatish
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Barcha fayllarni nusxalash
COPY . .

CMD ["python", "bot.py"]