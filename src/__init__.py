import os
from importlib import import_module
from pathlib import Path

from flask import Flask
from flask_migrate import Migrate

from src.config import Config

from dotenv import dotenv_values

config =  dotenv_values("config.env")
app = Flask(__name__, instance_relative_config=True)
app.config.from_object(Config)

def register_blueprint(app):
    root_folder = Path.cwd().absolute()
    api_folder = os.path.join(root_folder, "src/api")
    sub_api_folder = [name for name in os.listdir(api_folder) if os.path.isdir(os.path.join(api_folder, name))]
    for module_name in sub_api_folder:
        if module_name == '__pycache__':
            continue
        module = import_module('src.api.{}.routes.routes'.format(module_name))
        print(module)
        app.register_blueprint(module.blueprint)

def create_app():
    with app.app_context():
        register_blueprint(app=app)
    return app