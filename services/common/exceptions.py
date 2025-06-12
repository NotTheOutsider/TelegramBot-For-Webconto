# exceptions.py
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
import logging

logger = logging.getLogger(__name__)

async def http_exception_handler(request: Request, exc: HTTPException):
    body_content = None
    try:
        if request.method in ["POST", "PUT", "PATCH"]:
            body_content = await request.json()
    except Exception:
        body_content = await request.body()
        if body_content:
            body_content = body_content.decode('utf-8', errors='ignore')
        else:
            body_content = "[No Request Body]"

    if exc.status_code == 400:
        logger.error( # Use warning for client-side errors
            f"Client Error (400 Bad Request): {exc.detail}\n"
            f"  Request URL: {request.url}\n"
            f"  Method: {request.method}\n"
            f"  Headers: {dict(request.headers)}\n"
            f"  Request Body: {body_content}"
        )
    elif exc.status_code == 401:
        logger.error( # Maybe info for unauthorized, not a server error
            f"Authentication Error (401 Unauthorized): {exc.detail}\n"
            f"  Request URL: {request.url}"
        )
    else: # For all other HTTPExceptions (e.g., 404, 422, 500 etc.)
        logger.error(
            f"HTTP Exception Occurred: {exc.status_code} - {exc.detail}\n"
            f"  Request URL: {request.url}\n"
            f"  Method: {request.method}\n"
            f"  Headers: {dict(request.headers)}\n"
            f"  Request Body: {body_content}"
        )

    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )