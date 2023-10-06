# -*- coding: utf-8 -*-
import logging
import os
from app.configs import settings
from fastapi import APIRouter


router = APIRouter(tags=['Views'])
# logger = logging.getLogger(constants.LOG_NAME_API_APP_USER)


@router.post("/ping")
async def ping():
       return "pong"
