from fastapi import FastAPI, Depends
from fastapi import FastAPI, Request, status
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from api.account import account_api
from api.users import user_api
from api.scheduling import scheduling_api
# from log_setting import logger

import time


def include_router(app):
    app.include_router(account_api.router, prefix="/api/account")
    app.include_router(user_api.router, prefix="/api/user")
    app.include_router(scheduling_api.router, prefix="/api/scheduling")


def start_application():
    app = FastAPI()
    origins = ["*"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    include_router(app)
    # app.mount('/static/images', StaticFiles(directory="static/images", html=True), name="static")
    return app


app = start_application()
