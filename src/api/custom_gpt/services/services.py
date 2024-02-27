import os, io, json

import requests
from ....static import constants
from ....config import Config

def upload_file_to_customgpt(file_name, file_path):
    def get_api_key_from_file():
        if(os.path.exists('keys/custom-gpt-keys.json')):
            keys_folder = os.path.join(os.path.join(os.getcwd(), 'keys'), 'custom-gpt-keys.json')
            with open(keys_folder) as key_file:
                data = json.load(key_file)
                return True, data['key']
        return False, None
    try:
        status, api_key = get_api_key_from_file()
        headers = {
            "accept": "application/json",
            "authorization": api_key
        }
        body = {
            'file_data_retention': True
        }
        files = None
        with open(file_path, 'rb') as input_file:
            files = {'file': input_file}
            upload_file_url = f'{constants.CUSTOM_GPT_URL}{Config.CUSTOM_GPT_PROJECT_ID}/sources'
            responses = requests.post(url=upload_file_url,headers=headers,files=files, json=body)
            print(responses.json())
            if responses.status_code == 200:
                return {
                    'status': 200,
                    'message': 'Upload successfull'
                }
    except Exception as error:
        print(f"An error occured: {error}")
