#! /usr/bin/env sh
# Run migrations
alembic upgrade head

# Create initial data in DB
python scripts/init_data.py

uvicorn "src.main:app" "--host" "0.0.0.0" "--port" "80" "--root-path" ${ASGI_ROOT_PATH}
