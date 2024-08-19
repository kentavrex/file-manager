import logging.config
from os import path

import uvicorn
from fastapi import FastAPI

from api.middleware import HandleHTTPErrorsMiddleware
from api.routes import documents

log_file_path = path.join(path.dirname(path.abspath(__file__)), "../log_config.ini")
logging.config.fileConfig(log_file_path, disable_existing_loggers=False)
logging.getLogger().setLevel(logging.INFO)

app = FastAPI(title="File-Manager")

# Middlewares
app.add_middleware(HandleHTTPErrorsMiddleware)

# App routes
app.include_router(documents.router, prefix="/documents", tags=["documents"])

if __name__ == "__main__":
    uvicorn.run(app, reload=True)
