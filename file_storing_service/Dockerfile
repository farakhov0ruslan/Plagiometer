# file_storing_service/Dockerfile
FROM python:3.11-slim

# 1) Системные зависимости для psycopg2 (Postgres) и компиляции C-расширений
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      build-essential gcc libpq-dev \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app
ENV PYTHONPATH=/app

# 2) Устанавливаем Python-зависимости
COPY requirements.txt .
RUN pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# 3) Копируем код внутрь подпапки file_storing_service
COPY . /app/file_storing_service

EXPOSE 80

# 4) Запускаем Uvicorn, импортируя модуль из подпапки
CMD ["uvicorn", "file_storing_service.main:app", "--host", "0.0.0.0", "--port", "80"]
