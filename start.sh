#!/bin/sh
alembic upgrade head
cd src
uvicorn main:app --host 0.0.0.0 --root-path /api/file_manager --log-config ../log_config.ini
