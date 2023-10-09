from __future__ import print_function
import os
import io
import sys
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# スコープを変更してファイルのアップロードを許可する
SCOPES = [
  'https://www.googleapis.com/auth/drive',
  'https://www.googleapis.com/auth/drive.file',
  'https://www.googleapis.com/auth/drive.appdata'
]

def upload_to_folder(service, filename):
    folder_id = 'xxxxxxxxxxxxxxym'  # TODO: 実際のフォルダIDを設定してください
    file_metadata = {
        'name': filename,
        'parents': [folder_id]
    }

    media = MediaFileUpload(os.path.join(os.getcwd()+"/../harvest/", filename))
    try:
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        print('File ID:', file.get('id'))
    except HttpError as error:
        # TODO(developer) - Handle error.
        print(f'An error occurred: {error}')

def main():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('drive', 'v3', credentials=creds)

    # コマンドライン引数からファイル名を取得
    if len(sys.argv) != 2:
        print('Usage: python script.py <filename>')
        sys.exit(1)

    filename = sys.argv[1]
    upload_to_folder(service, filename)

if __name__ == '__main__':
    main()
