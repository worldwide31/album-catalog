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
