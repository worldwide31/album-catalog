# Album Catalog

Простое веб-приложение "Каталог альбомов".

Поля альбома:

- название альбома
- исполнитель
- год
- оценка от 1 до 10

## Цель проекта

Проект показывает:

- разделение кода и конфигурации;
- отсутствие локальных абсолютных путей вроде `C:\Users\...` или `/home/user/...`;
- структуру одного репозитория для одного приложения;
- использование веток `staging` и `prod` как частей одной кодовой базы.

## Структура

```text
album-catalog/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── db.py
│   ├── routes.py
│   ├── services.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── form.html
│   │   └── index.html
│   └── static/
│       └── style.css
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
└── run.py
```

## Запуск

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Установка зависимостей:

```bash
pip install -r requirements.txt
```

Создайте файл `.env` на основе `.env.example`:

```bash
cp .env.example .env
```

Запуск приложения:

```bash
python run.py
```

После запуска откройте:

```text
http://127.0.0.1:5000
```

## Git

```bash
git init
git add .
git commit -m "Initial album catalog app"
git branch staging
git branch prod
git branch
```

Переключение между ветками:

```bash
git checkout staging
git checkout prod
git checkout main
```

## Docker

Приложение подготовлено для запуска в контейнере Docker.

### Что было изменено

- приложение слушает адрес `0.0.0.0`;
- порт задаётся через переменную окружения `PORT`;
- добавлен `Dockerfile`;
- добавлен `.dockerignore`;
- зависимости устанавливаются внутри контейнера.

### Сборка образа

```bash
docker build -t album-catalog .
```

### Запуск контейнера

```bash
docker run --name album-catalog-container -p 8080:5000 -e PORT=5000 album-catalog
```

После запуска откройте в браузере:

```text
http://localhost:8080
```

### Остановка контейнера

Вариант 1: нажать `Ctrl+C` в терминале, где запущен контейнер.

Вариант 2: из другого терминала выполнить:

```bash
docker stop album-catalog-container
```

### Повторный запуск контейнера

```bash
docker start album-catalog-container
```

### Удаление контейнера

```bash
docker rm album-catalog-container
```

Если контейнер ещё работает:

```bash
docker rm -f album-catalog-container
```

### Пересборка образа

Даже если удалить `.venv` из проекта, образ соберётся снова, потому что зависимости устанавливаются внутри Docker:

```bash
docker build -t album-catalog .
```

## Практика 3: конфигурация через переменные окружения

Настройки приложения вынесены из кода.

Используемые переменные:

| Переменная | Назначение | Значение по умолчанию |
|---|---|---|
| `APP_NAME` | Название приложения | `Каталог альбомов` |
| `HOST` | Хост приложения | `0.0.0.0` |
| `PORT` | Порт приложения | `5000` |
| `FLASK_ENV` | Режим запуска | `production` |
| `SECRET_KEY` | Секретный ключ Flask | `change-me-only-for-local-dev` |
| `DATABASE_URL` | Строка подключения к БД | `sqlite:///albums.db` |
| `CONFIG_FILE` | YAML-файл конфигурации | `config.yaml` |

Для локальной разработки можно создать файлы:

```bash
copy .env.example .env
copy config.yaml.example config.yaml
```

На macOS/Linux:

```bash
cp .env.example .env
cp config.yaml.example config.yaml
```

Переменные окружения имеют приоритет над `config.yaml`.

### Сборка образа

```bash
docker build -t album-catalog:config .
```

### Запуск dev-окружения

```bash
docker run --rm --name album-catalog-dev -p 8080:5000 ^
  -e APP_NAME="Каталог альбомов DEV" ^
  -e PORT=5000 ^
  -e FLASK_ENV=development ^
  -e SECRET_KEY=dev-secret-example ^
  -e DATABASE_URL=sqlite:///albums_dev.db ^
  album-catalog:config
```

Открыть:

```text
http://localhost:8080
```

### Запуск prod-окружения тем же образом

```bash
docker run --rm --name album-catalog-prod -p 8080:7000 ^
  -e APP_NAME="Каталог альбомов PROD" ^
  -e PORT=7000 ^
  -e FLASK_ENV=production ^
  -e SECRET_KEY=prod-secret-example ^
  -e DATABASE_URL=sqlite:///albums_prod.db ^
  album-catalog:config
```

В этом случае образ не пересобирается. Меняются только переменные окружения.
