import logging

from gunicorn_loguru.intercept import InterceptHandler

INTERCEPTS = ["uvicorn", "uvicorn.access"]


def init():
    """Configures gunicorn loggers to use loguru."""
    for log in INTERCEPTS:
        logging.getLogger(log).handlers = [InterceptHandler()]
