
## Free deployment: GitHub + Koyeb

This project is configured for a Django/Gunicorn deployment from GitHub to Koyeb.

### Build command

```bash
bash build.sh
```

### Start command

```bash
bash start.sh
```

### Required environment variables

- `DJANGO_SECRET_KEY` — generate a long random value.
- `DEBUG=False`
- `ALLOWED_HOSTS` — include the Koyeb public hostname.
- `CORS_ALLOWED_ORIGINS` — set this only if a separate frontend calls the API.
- `DATABASE_URL` — optional; when absent, SQLite is used.

### Health check

`GET /health/`

### Important storage note

Koyeb free instances do not provide persistent local storage. Uploaded datasets,
trained model files, generated reports, and SQLite data can be lost when the
instance is replaced or redeployed. Use PostgreSQL/object storage for persistent
production data.
