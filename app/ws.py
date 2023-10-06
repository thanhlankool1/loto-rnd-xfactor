# -*- coding: utf-8 -*-

import socketio
from app.configs import settings

sio = socketio.AsyncServer(
    async_mode="asgi",
    # ``'*'`` to allow all origins, or to ``[]`` to disable CORS handling, tested,
    cors_allowed_origins=settings.WS_SERVER_CORS_ORIGINS,
    logger=settings.WS_SERVER_ENABLE_DEBUGGING,  # for debbuging
    engineio_logger=settings.WS_SERVER_ENABLE_DEBUGGING,  # for debugging
    # for upload file size limitation
    max_http_buffer_size=settings.WS_SERVER_MAX_FILE_SIZE,
    ping_timeout=settings.WS_SERVER_PING_TIMEOUT,
    ping_interval=settings.WS_SERVER_PING_INTERVAL,
)
socketio_app = socketio.ASGIApp(socketio_server=sio, socketio_path=settings.WS_SERVER_SOCKETIO_PATH)


def initialize_socketio_event_handlers():
    from app.utils.ws_socketio import ws_event_mapping

    for event_name, event_config in ws_event_mapping.items():
        sio.on(
            event_name,
            event_config.get("handler"),
            event_config.get("namespace"),
        )
        print(f"add socketio event {event_name} -> {event_config}")
