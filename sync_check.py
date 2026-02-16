import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

def main():
    config_path = 'antigravity.yaml'
    creds_path = 'credentials/novel-antigravity-sync-de1513029e5a.json'
    folder_id = '1F5tAWZg_i7r2MuK6YSOMCthHMBe8Ihvr'

    print(f"--- Diagnostic Report ---")
    
    # Check credentials file
    if not os.path.exists(creds_path):
        print(f"[ERROR] Credentials file not found at {creds_path}")
        return
    print(f"[OK] Credentials file found.")

    try:
        # Load credentials
        creds = service_account.Credentials.from_service_account_file(
            creds_path, scopes=['https://www.googleapis.com/auth/drive.readonly']
        )
        service = build('drive', 'v3', credentials=creds)

        # Try to list files in the folder
        print(f"[INFO] Attempting to access folder ID: {folder_id}")
        results = service.files().list(
            q=f"'{folder_id}' in parents and trashed = false",
            fields="nextPageToken, files(id, name)"
        ).execute()
        
        items = results.get('files', [])
        if not items:
            print("[WARNING] No files found in the folder.")
        else:
            print(f"[OK] Found {len(items)} files in folder:")
            for item in items:
                print(f" - {item['name']} ({item['id']})")

    except Exception as e:
        print(f"[ERROR] An error occurred: {e}")

if __name__ == '__main__':
    main()
