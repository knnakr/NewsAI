from collections import defaultdict
import time

from fastapi import Request
from fastapi.responses import JSONResponse


_request_counts: dict[str, list[float]] = defaultdict(list)
WINDOW_SECONDS = 60
MAX_REQUESTS = 10


async def rate_limit_middleware(request: Request, call_next):
	if request.url.path.startswith("/auth"):
		client_ip = request.client.host if request.client else "unknown"
		key = f"{client_ip}:{request.method}:{request.url.path}"
		now = time.time()
		window_start = now - WINDOW_SECONDS
		_request_counts[key] = [t for t in _request_counts[key] if t > window_start]

		if len(_request_counts[key]) >= MAX_REQUESTS:
			return JSONResponse(status_code=429, content={"detail": "Cok fazla istek. Bir dakika bekleyin."})

		response = await call_next(request)
		if response.status_code >= 400:
			_request_counts[key].append(now)
		return response

	return await call_next(request)
