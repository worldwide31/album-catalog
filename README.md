# Album Catalog

Простое веб-приложение **«Каталог альбомов»**.

Поля альбома:

- название альбома;
- исполнитель;
- год;
- оценка от 1 до 10.

## Практика 5: сборка, релиз, запуск и масштабирование

В проект добавлены:

- GitHub Actions workflow для сборки и публикации Docker-образа;
- уникальные теги образа по commit hash и номеру сборки;
- публикация образа в GitHub Container Registry;
- release workflow без пересборки образа;
- `docker-compose.release.yml` для запуска фиксированного образа с runtime-конфигурацией;
- Redis для централизованного хранения сессий;
- PostgreSQL для хранения состояния приложения;
- Nginx как reverse proxy;
- скрипт нагрузочной проверки `scripts/load_test.py`.

## Локальный запуск через Docker Compose

```bash
docker compose up --build
```

Открыть:

```text
http://localhost:8080
```

Health endpoint:

```text
http://localhost:8080/health
```

Проверка централизованных сессий:

```text
http://localhost:8080/session-demo
```

## Масштабирование

```bash
docker compose up --build --scale app=3
```

Проверка распределения запросов:

```bash
python scripts/load_test.py
```

В выводе должны появляться разные значения `instance`.

## Release без пересборки

Сначала GitHub Actions публикует образ, например:

```text
ghcr.io/worldwide31/album-catalog:sha-a1b2c3d
```

Затем этот же образ можно запускать с разной конфигурацией.

Пример staging:

```bash
copy .env.staging.example .env.staging
```

В файле `.env.staging` нужно заменить:

```text
sha-CHANGE_ME
```

на реальный тег образа.

Запуск:

```bash
docker compose --env-file .env.staging -f docker-compose.release.yml up --scale app=3
```

Пример production:

```bash
copy .env.prod.example .env.prod
docker compose --env-file .env.prod -f docker-compose.release.yml up --scale app=3
```

## GitHub Actions

Файл сборки:

```text
.github/workflows/docker-image.yml
```

Он запускается при push в `main`, собирает Docker-образ и публикует его в GHCR с тегами:

- `sha-<commit_hash>`;
- `build-<run_number>`;
- `latest`.

Файл релиза:

```text
.github/workflows/release.yml
```

Он запускается вручную через `workflow_dispatch`, принимает:

- окружение;
- фиксированный тег образа.

Релиз не пересобирает образ, а только применяет runtime-конфигурацию.
