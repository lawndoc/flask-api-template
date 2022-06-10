import os


class Config(object):
    APP_NAME = os.environ.get("APP_NAME") or "Flask App"
    LOG_LEVEL = int(os.environ.get("LOG_LEVEL") or 4)