from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

from app.mod_web import mod_web as web_module
app.register_blueprint(web_module)
