FROM python:3.11-slim

# Установка зависимостей системы
RUN apt-get update && apt-get install -y build-essential libpq-dev && apt-get clean

# Установка рабочей директории
WORKDIR /app

# Копируем зависимости
COPY requirements.txt .

# Установка зависимостей Python
RUN pip install --no-cache-dir -r requirements.txt

# Копируем проект
COPY . .

# Открываем порт
EXPOSE 8000

# Команда запуска
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
