import os

basedir = os.path.abspath(os.path.dirname(__file__))
print('{}://{}:{}@{}:{}/{}'.format(
        os.getenv('DB_ENGINE'   , 'postgresql'),
        os.getenv('DB_USERNAME' , 'appseed_db_usr'),
        os.getenv('DB_PASSWORD' , 'pass'),
        os.getenv('DB_HOST'     , 'localhost'),
        os.getenv('DB_PORT'     , 5432),
        os.getenv('DB_NAME'     , 'appseed_db')
))

class Config(object):
    DEBUG = os.getenv("DEBUG") or False
    TESTING = os.getenv("TESTING") or False
    SECRET_KEY = os.getenv('SECRET_KEY') 
    CUSTOM_GPT_PROJECT_ID = os.getenv('CUSTOMGPT_PROJECT_ID') or '20803'
    API_KEY_PATH = os.getenv('API_KEY_PATH') or '/Users/khoanguyennhat/Pmax/Flask_GCP/keys/kms-chatbot-f6b2c92cc678.json'

class ProductionConfig(Config):
    DEBUG = False

class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
