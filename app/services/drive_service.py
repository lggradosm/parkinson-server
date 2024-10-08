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

def list_files():
    creds = load_credentials()
    service = build('drive', 'v3', credentials=creds)

    # Llama a la API de Google Drive
    results = service.files().list(pageSize=10, fields="files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        return {"message": "No files found."}
    else:
        files_list = [{"name": file['name'], "id": file['id']} for file in items]
        return {"files": files_list}

def upload_file_to_drive(file_stream, file_name):
    creds = load_credentials()
    folder_id = "1ohJ3h3iCJ9h2lDuMENOYnqYq-2aajTVM"
    service = build('drive', 'v3', credentials=creds)
    file_metadata = {
        'name': file_name,  # Nombre del archivo
        'parents': [folder_id]  # ID de la carpeta donde subirás el archivo
    }
    media = MediaIoBaseUpload(file_stream, mimetype='audio/wav', resumable=True)
    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()
    return file.get('id')

def download_file (file_id):
    creds = load_credentials()
    service = build('drive', 'v3', credentials=creds)
    request = service.files().get_media(fileId=file_id)
    file_io = BytesIO()
    downloader = MediaIoBaseDownload(file_io, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
        print(f"Descargando {int(status.progress() * 100)}%")
    # Reposicionar el puntero al inicio del archivo en memoria
    file_io.seek(0)
    return file_io