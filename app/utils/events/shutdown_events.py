# -*- coding: utf-8 -*-
# from tortoise import Tortoise

async def event_99_notify_app_stopped():
    print('FastApi-Celery-App Stopped')


events = [v for k, v in locals().items() if k.startswith('event_')]
