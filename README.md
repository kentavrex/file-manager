# File-manager

Application to manage (store, get, remove) your files with any extension.

Use Swagger to feel good :)

## Stack
- **Python3.12**
- **FastApi** framework
- **PostgreSQL** DB
- **SQLAlchemy** ORM
- **Alembic** migrations
- **aioboto3** for work with s3
- **Redis** for cache
- **Celery** for background and scheduled tasks
- **Pydantic** for validation
- **pytest** for tests
- **punq** for DI containers pattern

## Dependencies

- Docker
- Docker compose

## Running
1. `docker compose up --build`
2. Open `http://localhost:9001/` with minioadmin:minioadmin creds
3. Create _documents_ bucket

- Base URL: `http://localhost:3006/`
- Swagger URL: `http://localhost:3006/docs`
- Minio (UI for S3) URL: `http://localhost:9001/`


Endpoints:
- GET /documents/{document_id}
- POST /documents

Database tables:
- documents

## Swagger

![swagger_screenshot](readme_data/swagger.png)

## Upload files

![image](readme_data/upload0.png)

DB (metadata with UID):
![image](readme_data/upload1.png)

Disk storage:
![image](readme_data/upload4.png)

S3 storage (Mino web UI):
![image](readme_data/upload2.png)

Stream uploading by 1024 bytes parts:
![image](readme_data/upload3.png)

## Get file
File metadata + download link
![image](readme_data/get1.png)

Put download link to browser:
![image](readme_data/get2.png)
![image](readme_data/get3.png)


## Celery task to remove useless files on schedule
Task run every day on midnight:
![image](readme_data/celery0.png)

Example:
![image](readme_data/celery1.png)

