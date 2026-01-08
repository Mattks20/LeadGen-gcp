#!/usr/bin/env python3
"""
Simple test script to verify Google Sheets authentication works.
Writes a test row to verify Workload Identity Federation is configured correctly.
"""

import os
from datetime import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
import google.auth

def main():
    # Get Sheet ID from environment variable
    sheet_id = os.environ.get('GOOGLE_SHEET_ID')
    
    if not sheet_id:
        raise ValueError("GOOGLE_SHEET_ID environment variable not set")
    
    print(f"Authenticating to Google Sheets...")
    print(f"Sheet ID: {sheet_id}")
    
    # Use Application Default Credentials (set by google-github-actions/auth)
    credentials, project = google.auth.default(
        scopes=['https://www.googleapis.com/auth/spreadsheets']
    )
    
    print(f"Authenticated with project: {project}")
    
    # Build the Sheets API client
    service = build('sheets', 'v4', credentials=credentials)
    
    # Prepare test data
    timestamp = datetime.now().isoformat()
    test_data = [
        ['Test Company Inc.', 'Authentication Successful', timestamp]
    ]
    
    # Write to sheet
    print("Writing test data to sheet...")
    body = {
        'values': test_data
    }
    
    result = service.spreadsheets().values().append(
        spreadsheetId=sheet_id,
        range='A:C',
        valueInputOption='RAW',
        body=body
    ).execute()
    
    print(f"✅ Success! Added {result.get('updates').get('updatedRows')} row(s)")
    print(f"Updated range: {result.get('updates').get('updatedRange')}")
    print("\n🎉 Google Sheets integration is working!")

if __name__ == '__main__':
    main()
