#!/bin/bash
# Run migrations
alembic upgrade head

# Start the application
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:10000
