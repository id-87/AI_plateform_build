# # drive_service.py

# import io
# from google.oauth2 import service_account
# from googleapiclient.discovery import build
# from googleapiclient.http import MediaIoBaseDownload
# from pypdf import PdfReader

# SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]


# class DriveService:
#     def __init__(self, credentials_path="credentials.json"):
#         creds = service_account.Credentials.from_service_account_file(
#             credentials_path, scopes=SCOPES
#         )
#         self.service = build("drive", "v3", credentials=creds)

#     def list_files(self, folder_id):
#         query = f"'{folder_id}' in parents and trashed=false"

#         results = self.service.files().list(
#             q=query,
#             fields="files(id, name, mimeType)"
#         ).execute()

#         return results.get("files", [])

#     def download_file(self, file_id):
#         request = self.service.files().get_media(fileId=file_id)

#         fh = io.BytesIO()
#         downloader = MediaIoBaseDownload(fh, request)

#         done = False
#         while not done:
#             _, done = downloader.next_chunk()

#         fh.seek(0)
#         return fh

#     def extract_text(self, file_stream, mime_type):
#         if mime_type == "application/pdf":
#             reader = PdfReader(file_stream)
#             return "\n".join([page.extract_text() or "" for page in reader.pages])

#         elif mime_type == "text/plain":
#             return file_stream.read().decode("utf-8")

#         return None


# services/drive_service.py

import json
import base64
import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]


class DriveService:
    def __init__(self):
        creds = self._load_credentials()
        self.service = build("drive", "v3", credentials=creds)

    def _load_credentials(self):
        b64 = st.secrets["GOOGLE_CREDENTIALS_BASE64"]
        info = json.loads(base64.b64decode(b64))

        return service_account.Credentials.from_service_account_info(
            info,
            scopes=SCOPES
        )