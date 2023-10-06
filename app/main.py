# -*- coding: utf-8 -*-
from fastapi import FastAPI
from .api import app as api_app
from app.utils.events import startup_event, shutdown_event
# from app.core.database.minio import minio_client
from .ws import initialize_socketio_event_handlers, socketio_app


app = FastAPI(
    on_startup=startup_event,
    on_shutdown=shutdown_event,
    docs_url=None,
    )


# mount websocket
app.mount("/ws", socketio_app)
initialize_socketio_event_handlers()

# mount api app
app.mount("/", api_app)

