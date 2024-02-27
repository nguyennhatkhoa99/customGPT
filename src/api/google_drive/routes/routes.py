import json, os

from flask_restful import Resource
from flask import request, jsonify

from src.api.google_drive import blueprint_api, blueprint
from ..services.services import init_connection, get_file
from ....config import Config
from ....static.constants import TMP_FOLDER


class GGDriveAPI(Resource):
    def get(self, id):
        try:
            gg_service = init_connection(token_file_path=Config.API_KEY_PATH)
            file_info = get_file(gg_service, id, is_download=False)
            file_content = get_file(gg_service, id)
            saved_file_path = os.path.join(os.path.join(os.getcwd(), TMP_FOLDER), file_info.__dict__['name'])
            with open(saved_file_path, 'wb') as write_file:
                write_file.write(file_content)
            return {
                "data": file_info.__dict__,
                "status": 200,
                "message": "Download File successful"
            }

        except Exception as error:
            return {
                "data": None,
                "status": "error",
                "message": str(error)
            }
        

blueprint_api.add_resource(GGDriveAPI, '/gg/<string:id>')

