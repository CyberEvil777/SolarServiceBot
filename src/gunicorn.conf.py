import os

bind = "0.0.0.0:8001"
workers = os.getenv("GUNICORN_WORKERS", 3)
reload = True
