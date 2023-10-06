# -*- coding: utf-8 -*-
# from app.core.database.sql import connect_databases
import logging

async def event_01_create_debug_logger():
    # await connect_databases()
    return

async def event_99_notify_app_started():
    print("ok")
    return

events = [v for k, v in locals().items() if k.startswith('event_')]