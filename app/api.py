# -*- coding: utf-8 -*-
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.exceptions import RequestValidationError
from app.utils.exceptions import ErrorResponseException
from app.utils.exceptions import ErrorHtmlResponseException
from app.utils.middlewares import *
from fastapi.staticfiles import StaticFiles
from app.configs import settings
from app.views import router as loto

# patch aiohttp proxy
# https://github.com/aio-libs/aiohttp/discussions/6044
import asyncio
setattr(asyncio.sslproto._SSLProtocolTransport, "_start_tls_compatible", True)


# declare APP
app = FastAPI(
    title='LOTO-RnD',
    description="Chơi Là Trúng",
    middleware=None,
    docs_url=settings.APP_DOCS_URL,
    openapi_url='/api/openapi.json',
    redoc_url=None
)

# static files
app.mount("/statics", StaticFiles(directory="statics"), name="statics")



# add custom exception handlers
@app.exception_handler(ErrorResponseException)
async def error_response_exception_handler(request: Request, exception: ErrorResponseException):
    return JSONResponse(
        status_code=exception.status_code,
        content={
            "success": exception.success,
            "data": exception.data,
            "length": exception.length,
            "error": exception.error,
            "error_code": exception.error_code
        },
    )


@app.exception_handler(ErrorHtmlResponseException)
async def error_response_exception_handler(request: Request, exception: ErrorHtmlResponseException):  # noqaF811
    return HTMLResponse(f'<h1>{exception.error}</h1>')


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError, error_code=8000):
    try:
        msg = "miss field required: "
        for i in exc.errors():
            #msg += f'{i.get("msg")}: {i.get("loc")[1]}, '
            msg += f'{i.get("loc")[-1]}, '
    except Exception as e:
        msg = f'unknown exception {e} when handling exception {exc}'
    return JSONResponse(
        status_code=200,
        content={
            "success": False,
            "data": [],
            "length": 1,
            "error": msg,
            "error_code": error_code,
        },
    )


# add routers
for router in (
    {'module': loto, 'prefix': '/loto', },
):
    app.include_router(
        router.get('module'),
        prefix=router.get('prefix'),
        tags=router.get('tags')
    )


@app.get("/")
async def root():
    return {"message": "Hello VoiceBotCampaign Applications!"}
items = {}

@app.get("/hello")
async def root():
    return {"message": f"Hello VoiceBotCampaign Applications! {items}"}
