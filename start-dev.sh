#!/bin/sh
alembic upgrade head
cd src
uvicorn main:app --host 0.0.0.0 --log-config ../log_config.ini --reload
