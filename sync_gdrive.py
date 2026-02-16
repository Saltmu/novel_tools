import os
import io
import time
import sys
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

CACHE_FILE = '.sync_cache'
LOCK_FILE = '.sync.lock'
CACHE_DURATION = 300  # 5 minutes in seconds

def main():
    # Check if another process is already syncing
    if os.path.exists(LOCK_FILE):
        print("Another sync process is running. Waiting or skipping...")
        # Wait a bit or skip
        return

    # Check cache
    if os.path.exists(CACHE_FILE):
        last_sync = os.path.getmtime(CACHE_FILE)
        if time.time() - last_sync < CACHE_DURATION:
            print("Recently synced. Skipping...")
            return

    try:
        # Create lock
        with open(LOCK_FILE, 'w') as f:
            f.write(str(os.getpid()))

        creds_path = 'credentials/novel-antigravity-sync-de1513029e5a.json'
        folder_id = '1F5tAWZg_i7r2MuK6YSOMCthHMBe8Ihvr'
        output_dir = 'data/sources'

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        creds = service_account.Credentials.from_service_account_file(
            creds_path, scopes=['https://www.googleapis.com/auth/drive.readonly']
        )
        service = build('drive', 'v3', credentials=creds)

        print(f"Downloading files from folder: {folder_id}...")
        results = service.files().list(
            q=f"'{folder_id}' in parents and trashed = false",
            fields="files(id, name, mimeType)"
        ).execute()
        
        items = results.get('files', [])
        for item in items:
            name = item['name']
            file_id = item['id']
            mime_type = item['mimeType']

            print(f"Processing: {name} ({mime_type})")
            
            if mime_type == 'application/vnd.google-apps.document':
                request = service.files().export_media(fileId=file_id, mimeType='text/plain')
                file_path = os.path.join(output_dir, f"{name}.txt")
            else:
                request = service.files().get_media(fileId=file_id)
                file_path = os.path.join(output_dir, name)

            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
            
            with open(file_path, 'wb') as f:
                f.write(fh.getvalue())
            print(f"Saved to {file_path}")

        # Update cache timestamp
        with open(CACHE_FILE, 'w') as f:
            f.write(str(time.time()))

    finally:
        # Remove lock
        if os.path.exists(LOCK_FILE):
            os.remove(LOCK_FILE)

if __name__ == '__main__':
    main()
