"""
Google Sheets Workspace Integration Module

Handles authentication and operations with Google Sheets API.
Follows Project Lumina's requirement to use Service Account authentication.
"""

import json
import os
from typing import List, Dict, Any, Optional
from pathlib import Path
import logging

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


logger = logging.getLogger(__name__)


class WorkspaceManager:
    """
    Manages Google Sheets operations for Project Lumina.

    Uses Service Account authentication to read/write lead data,
    configuration, and logs to Google Sheets.
    """

    SCOPES = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive.file'
    ]

    def __init__(self, credentials_path: Optional[str] = None, spreadsheet_id: Optional[str] = None):
        """
        Initialize the WorkspaceManager.

        Args:
            credentials_path: Path to service account JSON file
            spreadsheet_id: Google Sheets spreadsheet ID
        """
        self.credentials_path = credentials_path or self._get_default_credentials_path()
        self.spreadsheet_id = spreadsheet_id or os.getenv('GOOGLE_SHEET_ID')
        self.service = None
        self._authenticate()

    def _get_default_credentials_path(self) -> str:
        """Get default path to service account credentials."""
        project_root = Path(__file__).parent.parent
        default_path = project_root / 'credentials' / 'service-account.json'
        return str(default_path)

    def _authenticate(self) -> None:
        """
        Authenticate with Google Sheets API using Service Account.

        Raises:
            FileNotFoundError: If credentials file doesn't exist
            ValueError: If credentials are invalid
        """
        if not os.path.exists(self.credentials_path):
            raise FileNotFoundError(
                f"Service account credentials not found at: {self.credentials_path}\n"
                f"Please place your service-account.json file in the credentials/ folder."
            )

        try:
            credentials = service_account.Credentials.from_service_account_file(
                self.credentials_path,
                scopes=self.SCOPES
            )
            self.service = build('sheets', 'v4', credentials=credentials)
            logger.info("Successfully authenticated with Google Sheets API")
        except Exception as e:
            raise ValueError(f"Failed to authenticate with Google Sheets API: {str(e)}")

    def test_connection(self) -> bool:
        """
        Test the connection to Google Sheets.

        Returns:
            bool: True if connection is successful
        """
        if not self.spreadsheet_id:
            logger.error("No spreadsheet ID configured. Set GOOGLE_SHEET_ID environment variable.")
            return False

        try:
            # Try to read spreadsheet metadata
            sheet_metadata = self.service.spreadsheets().get(
                spreadsheetId=self.spreadsheet_id
            ).execute()

            sheet_title = sheet_metadata.get('properties', {}).get('title', 'Unknown')
            logger.info(f"Successfully connected to spreadsheet: {sheet_title}")
            return True
        except HttpError as e:
            logger.error(f"Failed to connect to spreadsheet: {str(e)}")
            return False

    def read_range(self, range_name: str) -> List[List[Any]]:
        """
        Read data from a specific range in the spreadsheet.

        Args:
            range_name: A1 notation range (e.g., 'Leads!A1:F100')

        Returns:
            List of rows, where each row is a list of cell values
        """
        try:
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.spreadsheet_id,
                range=range_name
            ).execute()

            values = result.get('values', [])
            logger.info(f"Read {len(values)} rows from {range_name}")
            return values
        except HttpError as e:
            logger.error(f"Failed to read range {range_name}: {str(e)}")
            return []

    def write_range(self, range_name: str, values: List[List[Any]],
                    value_input_option: str = 'USER_ENTERED') -> bool:
        """
        Write data to a specific range in the spreadsheet.

        Args:
            range_name: A1 notation range (e.g., 'Leads!A2:F2')
            values: List of rows to write
            value_input_option: How to interpret input ('RAW' or 'USER_ENTERED')

        Returns:
            bool: True if write was successful
        """
        try:
            body = {'values': values}
            result = self.service.spreadsheets().values().update(
                spreadsheetId=self.spreadsheet_id,
                range=range_name,
                valueInputOption=value_input_option,
                body=body
            ).execute()

            updated_cells = result.get('updatedCells', 0)
            logger.info(f"Updated {updated_cells} cells in {range_name}")
            return True
        except HttpError as e:
            logger.error(f"Failed to write to range {range_name}: {str(e)}")
            return False

    def append_rows(self, range_name: str, values: List[List[Any]],
                    value_input_option: str = 'USER_ENTERED') -> bool:
        """
        Append rows to the end of a sheet.

        Args:
            range_name: Sheet name or range (e.g., 'Leads!A:F')
            values: List of rows to append
            value_input_option: How to interpret input ('RAW' or 'USER_ENTERED')

        Returns:
            bool: True if append was successful
        """
        try:
            body = {'values': values}
            result = self.service.spreadsheets().values().append(
                spreadsheetId=self.spreadsheet_id,
                range=range_name,
                valueInputOption=value_input_option,
                insertDataOption='INSERT_ROWS',
                body=body
            ).execute()

            updated_range = result.get('updates', {}).get('updatedRange', '')
            logger.info(f"Appended {len(values)} rows to {updated_range}")
            return True
        except HttpError as e:
            logger.error(f"Failed to append to {range_name}: {str(e)}")
            return False

    def batch_update(self, updates: List[Dict[str, Any]]) -> bool:
        """
        Perform multiple write operations in a single batch.

        Args:
            updates: List of update dictionaries with 'range' and 'values' keys

        Returns:
            bool: True if batch update was successful
        """
        try:
            data = [
                {
                    'range': update['range'],
                    'values': update['values']
                }
                for update in updates
            ]

            body = {
                'valueInputOption': 'USER_ENTERED',
                'data': data
            }

            result = self.service.spreadsheets().values().batchUpdate(
                spreadsheetId=self.spreadsheet_id,
                body=body
            ).execute()

            total_updated = result.get('totalUpdatedCells', 0)
            logger.info(f"Batch updated {total_updated} cells across {len(updates)} ranges")
            return True
        except HttpError as e:
            logger.error(f"Failed to perform batch update: {str(e)}")
            return False

    def create_sheet(self, sheet_name: str) -> bool:
        """
        Create a new sheet in the spreadsheet.

        Args:
            sheet_name: Name of the new sheet

        Returns:
            bool: True if sheet creation was successful
        """
        try:
            request_body = {
                'requests': [{
                    'addSheet': {
                        'properties': {
                            'title': sheet_name
                        }
                    }
                }]
            }

            self.service.spreadsheets().batchUpdate(
                spreadsheetId=self.spreadsheet_id,
                body=request_body
            ).execute()

            logger.info(f"Created new sheet: {sheet_name}")
            return True
        except HttpError as e:
            if 'already exists' in str(e):
                logger.warning(f"Sheet '{sheet_name}' already exists")
                return True
            logger.error(f"Failed to create sheet {sheet_name}: {str(e)}")
            return False

    def setup_lead_sheet(self) -> bool:
        """
        Set up the standard Leads sheet with headers.

        Returns:
            bool: True if setup was successful
        """
        headers = [[
            'Company Name',
            'Contact Name',
            'Email',
            'Phone',
            'Score (Claude)',
            'Score (Secondary)',
            'Status',
            'Timestamp',
            'Notes'
        ]]

        # Create sheet if it doesn't exist
        self.create_sheet('Leads')

        # Write headers
        return self.write_range('Leads!A1:I1', headers)

    def setup_logs_sheet(self) -> bool:
        """
        Set up the Logs sheet for execution tracking.

        Returns:
            bool: True if setup was successful
        """
        headers = [[
            'Timestamp',
            'Event Type',
            'Message',
            'Status',
            'Details'
        ]]

        # Create sheet if it doesn't exist
        self.create_sheet('Logs')

        # Write headers
        return self.write_range('Logs!A1:E1', headers)

    def log_event(self, event_type: str, message: str, status: str = 'INFO',
                  details: str = '') -> bool:
        """
        Log an event to the Logs sheet.

        Args:
            event_type: Type of event (e.g., 'Discovery', 'Scoring', 'Error')
            message: Event message
            status: Status level (INFO, WARNING, ERROR)
            details: Additional details

        Returns:
            bool: True if logging was successful
        """
        from datetime import datetime

        timestamp = datetime.utcnow().isoformat()
        row = [[timestamp, event_type, message, status, details]]

        return self.append_rows('Logs!A:E', row)


def main():
    """Test the workspace connection."""
    import sys

    # Set up basic logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Test connection
    workspace = WorkspaceManager()

    if workspace.test_connection():
        print("✓ Google Sheets connection successful!")

        # Set up standard sheets
        print("\nSetting up standard sheet structure...")
        workspace.setup_lead_sheet()
        workspace.setup_logs_sheet()

        # Log a test event
        workspace.log_event('System', 'Workspace setup completed', 'INFO')

        print("✓ Sheet structure created successfully!")
        sys.exit(0)
    else:
        print("✗ Google Sheets connection failed!")
        print("\nPlease ensure:")
        print("1. Service account credentials are in credentials/service-account.json")
        print("2. GOOGLE_SHEET_ID environment variable is set")
        print("3. Service account has access to the spreadsheet")
        sys.exit(1)


if __name__ == '__main__':
    main()
