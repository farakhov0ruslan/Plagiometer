# Проект Plagiometr

**Кратко о задаче**

Данный проект состоит из трёх микросервисов:

1. **API Gateway** — прокси-сервис, объединяющий вызовы к сервисам хранения и анализа.
2. **File Storing Service** — сервис на FastAPI для загрузки, хранения и скачивания файлов (на дисковой системе + PostgreSQL).
3. **File Analysis Service** — сервис на FastAPI для анализа текстовых файлов: подсчёта слов, абзацев, символов и генерации облака слов (QuickChart Word Cloud API).

Основная цель: предоставить единый HTTP-интерфейс для клиента, скрывая детали внутреннего взаимодействия, а также реализовать чистую архитектуру (DDD + Clean Architecture).

---

## Структура микросервисов

```
/— api_gateway/               # API Gateway
   ├── main.py                # Точка входа FastAPI
   ├── routers/               # Роутеры (files, analysis)
   ├── services.py            # HTTP-клиенты для обращения к внутренним сервисам
   └── schemas.py             # Pydantic-модели запросов/ответов

/— file_storing_service/      # File Storing Service
   ├── main.py                # FastAPI-приложение
   ├── application/           # UseCases, DTOs, Ports
   ├── domain/                # Сущности, репозитории
   ├── infrastructure/        # SQLAlchemy, FS-Storage, Config
   └── presentation/          # Controllers (FastAPI роуты)

/— file_analysis_service/     # File Analysis Service
   ├── main.py                # FastAPI-приложение
   ├── application/           # UseCases, DTOs
   ├── domain/                # Сущности, репозитории, порты
   ├── infrastructure/        # DB, Local FS, WordCloudClient, Config
   └── presentation/          # Controllers (FastAPI роуты)
```

Каждый сервис:

* Разделён на слои: **presentation**, **application**, **domain**, **infrastructure**.
* Использует DDD: доменные сущности и репозитории вынесены в `domain`.
* Применяет принципы Clean Architecture: слои взаимодействуют через интерфейсы (ports).

---

## Запуск через Docker Compose

В корне проекта находится `docker-compose.yml`. Для старта всех сервисов выполните:

```bash
docker-compose down -v   # (опционально) очистить БД и данные
docker-compose up --build -d
```

Сервисы будут доступны на портах:

* **API Gateway**: `http://localhost:8000`
* File Storing Service (внутр. сеть): `http://file_service:80`
* File Analysis Service (внутр. сеть): `http://file_analysis_service:80`

Контейнеры автоматически создадут тома для баз данных и папок `data` (хранение файлов/картинок).

---

## Описание контейнеров

* **api\_gateway**: FastAPI, проксирует `/api/files/` и `/analysis/` к внутренним сервисам.
* **file\_service**: FastAPI, сохраняет файлы в `./data` и метаданные в PostgreSQL.
* **file\_analysis\_service**: FastAPI, анализирует текст, сохраняет результаты и генерирует облако слов.
* **file\_db** и **file\_analysis\_db**: PostgreSQL для хранения метаданных соответственно.

---

## API в Swagger

После поднятия сервисов, документация будет доступна:

* **API Gateway**: `http://localhost:8000/docs`
* **File Storing Service**: `http://localhost:8001/docs` (если порт проброшен)
* **File Analysis Service**: `http://localhost:8002/docs`

Я в настройках compose убрал возможность обращаться напрямую к сервисам, это нарушает логику Gateway
Там можно попробовать все endpoints: загрузка файлов, скачивание, анализ, получение облака слов.

---

### Обработка недоступности сервиса хранения

В реальной эксплуатации отдельные микросервисы могут временно «падать» или быть недоступны — важно, чтобы один сбой не обрушивал всю систему. В нашем случае:

* **Сервис анализа** зависит от **сервиса хранения** (он забирает по `file_id` содержимое файла),
* но **сервис хранения** сам по себе не зависит от анализа и должен продолжать работать даже при сбое анализа.

Поэтому мы ввели следующий механизм:

1. **На уровне Gateway** (или клиента) — все обращения к `file_service` оборачиваются в `try/except`:

   ```python
   try:
       resp = requests.request(..., url=f"{FILE_SERVICE_URL}/files/{file_id}")
       resp.raise_for_status()
   except requests.exceptions.RequestException as e:
       # не получилось дозвониться до file_service
       raise HTTPException(
           status_code=503,
           detail="Сервис хранения файлов временно недоступен. Попробуйте позже."
       )
   ```

2. **В контроллере анализа** мы ловим эту ошибку и переводим её в понятный клиенту ответ:

   ```python
   @router.get("/analysis/{file_id}")
   def analyze(...):
       try:
           return use_case.execute(...)
       except HTTPException as he:
           # если уже сформирован наш HTTPException (503 из storage), просто прокидываем
           raise
       except Exception as e:
           # все остальные ошибки анализатора
           raise HTTPException(status_code=500, detail=str(e))
   ```

3. **В логах** прописывается чёткая причина — именно «недоступен сервис хранения», а не «не удалось проанализировать файл»:

   ```
   ERROR 503: Сервис хранения файлов временно недоступен. Попробуйте позже.
   ```

---

Таким образом:

* Пользователь сразу получает понятный ответ о том, что **именно** сервис хранения недоступен,
* остальные части системы продолжают работать,
* при восстановлении хранения дальнейшие запросы к анализу и скачиванию файлов проходят без дополнительных настроек.


## Тестирование

В проекте используются **pytest**.

1. Установите dev-зависимости:

   ```bash
   pip install -r requirements-dev.txt
   ```
2. Запустите unit- и интеграционные тесты с отчётом покрытия:
   ```bash
   pytest
   ```

## Использованные принципы и инструменты

* **DDD (Domain-Driven Design)**:

  * `domain/entities.py`, `domain/repositories.py` для централизованного описания бизнес-моделей.
* **Clean Architecture**:
  * Четкое разделение на слои **presentation → application → domain → infrastructure**.
  * Зависимости направлены внутрь (use cases не зависят от FastAPI или SQLAlchemy напрямую).
* **FastAPI** для всех HTTP-интерфейсов, Pydantic для валидации.
* **SQLAlchemy ORM** для работы с PostgreSQL.
* **Docker & Docker Compose** для контейнеризации и оркестрации.
* **QuickChart Word Cloud API** для генерации облаков слов.

