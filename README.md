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
