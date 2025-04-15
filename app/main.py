import time
import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api import api_router
from fastapi.middleware.cors import CORSMiddleware

from app.exceptions import BaseHTTPException
import sys
sys.path.append("/usr/src/app/cluster-utils")

logger = logging.getLogger(__name__)

app = FastAPI(
            title='BH Catalog API',
            openapi_url='/api/v1/openapi.json',
            description="BH Catalog API is a RESTful API that provides endpoints to manage Metadata",
            version="1.0",
            debug=True,
        )

@app.exception_handler(BaseHTTPException)
def base_exception_handler(request: Request, exc: BaseHTTPException):
    logger.error(
        f'''An error occurred in application\n Error ID: {exc.id}\n Error Code: {exc.error_code}\n Error Message: {exc.formatted_message}'''
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.api_response,
        headers=exc.headers,
    )

app.include_router(
    api_router,
    prefix='/api/v1'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with the origin of your React frontend
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    print('Middleware is called')
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
