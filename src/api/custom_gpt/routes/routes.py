import json , os

from flask_restful import Resource
from flask import request

from src.api.custom_gpt import blueprint_api, blueprint
from ....config import Config
from ..services.services import upload_file_to_customgpt
from ....static.constants import TMP_FOLDER

class CustomGPTAPI(Resource):

    def post(self):
        try:
            body = request.json
            saved_file_path = os.path.join(os.path.join(os.getcwd(), TMP_FOLDER), body['name'])
            result = upload_file_to_customgpt(body['name'], saved_file_path)
            return result
            
        except Exception as error:
            return {
                "data": None,
                "status": "error",
                "message": str(error)
            }

        

blueprint_api.add_resource(CustomGPTAPI, '/customgpt/')