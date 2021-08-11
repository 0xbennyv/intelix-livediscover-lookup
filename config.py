import os
from dotenv import load_dotenv

load_dotenv()

class Config(object):
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    THREADS_PER_PAGE = 2
    CSRF_ENABLED = True
    CSRF_SESSION_KEY = os.urandom(256)
    JSON_SORT_KEYS = False
    SECRET_KEY = os.urandom(256)
    #3rd Party Integration
    INTELIX_CLIENT_ID = os.getenv('INTELIX_CLIENT_ID')
    INTELIX_CLIENT_SECRET = os.getenv('INTELIX_CLIENT_SECRET')
    