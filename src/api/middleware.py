import logging

from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from usecases.errors import (
    NotFoundError,
    PermissionsError,
    StorageConstraintError,
    StorageError,
    StorageFKError,
    ValidationError,
)


class HandleHTTPErrorsMiddleware(BaseHTTPMiddleware):
    @staticmethod
    async def dispatch(request: Request, call_next):  # noqa
        try:
            response = await call_next(request)
        except NotFoundError as e:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": str(e)})
        except StorageFKError as e:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"detail": str(e)})
        except StorageConstraintError as e:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"detail": str(e)})
        except ValueError as e:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"detail": str(e)})
        except ValidationError as e:
            return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content={"detail": str(e)})
        except PermissionsError as e:
            return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"detail": str(e)})
        except StorageError as e:
            logging.error(str(e))
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"detail": "Internal Server Error"},
            )
        except Exception as e:
            logging.error(e, exc_info=True)
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"detail": "Internal Server Error"},
            )
        return response
