# Лабораторна робота №1 — Віртуалізація та контейнеризація

## Проєкт
**DevOps Task Manager** — простий вебзастосунок для створення та виконання задач.

Архітектура:
- `frontend` — Nginx + HTML/JavaScript;
- `backend` — FastAPI + SQLAlchemy;
- `db` — PostgreSQL.

Таким чином, проєкт складається з трьох Docker-контейнерів.

## Вимоги
- Docker Desktop
- Docker Compose (входить до сучасного Docker Desktop)
- Git

## Запуск
У корені проєкту:

```bash
docker compose up --build
```

Після запуску:
- вебзастосунок: http://localhost:8080
- API: http://localhost:8000
- Swagger: http://localhost:8000/docs
- health check: http://localhost:8000/health

## Зупинка

```bash
docker compose down
```

Щоб також видалити дані PostgreSQL:

```bash
docker compose down -v
```

## Тести

Тести можна запускати локально в папці `backend`:

```bash
pip install -r requirements.txt
pytest -q
```

## GitHub

```bash
git init
git add .
git commit -m "Initial DevOps lab 1"
git branch -M main
git remote add origin https://github.com/LYarmoliuk/devops_task_manager.git
git push -u origin main
```
