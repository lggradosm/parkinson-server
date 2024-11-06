from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from fastapi import Request
from googleapiclient.http import MediaIoBaseUpload,MediaIoBaseDownload

from io import BytesIO


SCOPE = ['https://www.googleapis.com/auth/drive']
service_account_json_key = './parkinsondetectionapp-cc541e1c2038.json'

def load_credentials():
    creds = service_account.Credentials.from_service_account_file(
        filename=service_account_json_key
    )
    creds = creds.with_scopes(SCOPE)
    return creds

def upload_file_to_drive(file_stream, file_name):
    creds = load_credentials()
    folder_id = "1ohJ3h3iCJ9h2lDuMENOYnqYq-2aajTVM"
    service = build('drive', 'v3', credentials=creds)
    file_metadata = {
        'name': file_name, 
        'parents': [folder_id]
    }
    media = MediaIoBaseUpload(file_stream, mimetype='audio/wav', resumable=True)
    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()
    return file.get('id')
