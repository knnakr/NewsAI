"""
HTTP request/response logging middleware.
"""
import time
import logging
from fastapi import Request

logger = logging.getLogger("newsai")


async def logging_middleware(request: Request, call_next):
    """
    Logs HTTP request method, path, status code, and duration.
    
    Args:
        request: FastAPI request object
        call_next: Next middleware/route handler
        
    Returns:
        Response object with logged metadata
    """
    start = time.time()
    response = await call_next(request)
    duration = (time.time() - start) * 1000
    logger.info(
        f"{request.method} {request.url.path} → {response.status_code} ({duration:.0f}ms)"
    )
    return response
