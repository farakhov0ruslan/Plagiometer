FROM python:3.11-slim

# Системные зависимости для Postgres и сборки
RUN apt-get update \
 && apt-get install -y --no-install-recommends gcc libpq-dev \
 && rm -rf /var/lib/apt/lists/*

# Рабочая директория
WORKDIR /app
ENV PYTHONPATH=/app

# Зависимости Python
COPY requirements.txt .
RUN pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# Копируем весь код сразу в /app/file_analysis_service
COPY . /app/file_analysis_service
RUN mkdir -p data
# Порт и точка входа
EXPOSE 80
CMD ["uvicorn", "file_analysis_service.main:app", "--host", "0.0.0.0", "--port", "80"]

