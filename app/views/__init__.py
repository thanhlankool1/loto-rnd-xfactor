# -*- coding: utf-8 -*-
from fastapi import APIRouter
from .views import router as loto

router = APIRouter()

router.include_router(loto)