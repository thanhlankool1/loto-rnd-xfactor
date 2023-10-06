# -*- coding: utf-8 -*-
import argparse
import sys
import os
import uvloop
import uvicorn
from app.configs import settings

uvloop.install()

parser = argparse.ArgumentParser(description='Web App Configuration')
parser.add_argument(
    '--mode',
    dest='mode',
    default='api',
    help=f'mode api or audio stream, default api'
)

# parser
args = parser.parse_args()

if __name__ == '__main__':
    uvicorn.run(
        'app.main:app',
        loop='uvloop',
        reload=False,
        host=settings.GUNICORN_HOST,
        port=int(settings.GUNICORN_PORT),
        timeout_keep_alive=0 
    )
