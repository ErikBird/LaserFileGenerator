import os


class Config(object):
    ENV = os.environ['ENV']
    CSRF_ENABLED = True
    SECRET_KEY = "7ChZ9dqNUr75szvr7FQsBGeD7X9h7TC"



class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
