class Config(object):
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    DEBUG = True
    DB_NAME = 'sensor.db'
    SECRET_KEY = '\xde\xb5W\xee{\x8b\xed\xb4\xf2\x91\xcdP\xdfM\xeb02\xd4\xc5\x90mh\xad*'
    API_URL = ''