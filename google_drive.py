from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# ID de la carpeta destino
FOLDER_ID = "1WsqcBsH29oxdLNX4Srchctk0jAElNCNg"

def guardar_en_drive(nombre_archivo):
    creds = Credentials.from_authorized_user_file("token.json", ["https://www.googleapis.com/auth/drive"])
    service = build("drive", "v3", credentials=creds)

    file_metadata = {
        "name": nombre_archivo,
        "parents": [FOLDER_ID]
    }
    media = MediaFileUpload(nombre_archivo, mimetype="text/plain")
    file = service.files().create(body=file_metadata, media_body=media, fields="id").execute()
    return file.get("id")