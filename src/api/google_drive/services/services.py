import os, io

from ....utils.files import GoogleDriveFile

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload


SCOPES = ['https://www.googleapis.com/auth/drive']


def init_connection(token_file_path):
    creds = None
    if os.path.exists(token_file_path):
        creds = service_account.Credentials.from_service_account_file(token_file_path,scopes=SCOPES)
        creds = creds.with_subject('khoa.nguyen@pmax.com.vn')
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
    service = build("drive", "v3", credentials=creds)
    return service

def get_file(service, file_id, is_download=True):
    try: 
        
        file = io.BytesIO()
        if is_download:
            result = service.files().get_media(fileId=file_id)
            downloader = MediaIoBaseDownload(file, request=result)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print(f"Download {int(status.progress() * 100)}")
            return file.getvalue()  
        else:
            file_metadata_request = service.files().get(fileId=file_id)
            result = file_metadata_request.execute()
            file_info = GoogleDriveFile(
                id=result['id'],
                name=result['name'],
                mimeType=result['mimeType']
            )
            return file_info

    except HttpError as error:
        print(f"An error occured: {error}")
        print(error.status_code)
    
    
