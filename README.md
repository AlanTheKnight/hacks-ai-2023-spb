# NeoPitch

## Frontend

```
cd client
npm run dev
```

## Backend

```
cd backend
poetry run python manage.py runserver
```

### Celery

```
cd backend
poetry run python -m celery -A backend.celery worker -l info;
```
