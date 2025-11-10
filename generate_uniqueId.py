import gspread
from google.oauth2.service_account import Credentials
import uuid

# Setup Google Sheets authentication
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]
CREDENTIALS_FILE = "credentials.json"  # Download from Google Cloud Console
SPREADSHEET_NAME = "Spave8: Qr Codes"  # Change to your spreadsheet name
SHEET_NAME = "Sheet1"  # Change to your sheet name if different


def authenticate_google_sheets():
    """Authenticate and return Google Sheets client"""
    creds = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=SCOPES)
    return gspread.authorize(creds)


def create_unique_id():
    """Generate a unique ID"""
    return str(uuid.uuid4())


def add_unique_ids_to_sheet():
    """Add unique ID column to existing Google Sheet"""
    try:
        # Authenticate
        client = authenticate_google_sheets()

        # Open spreadsheet
        spreadsheet = client.open(SPREADSHEET_NAME)
        sheet = spreadsheet.worksheet(SHEET_NAME)

        # Get all values
        all_values = sheet.get_all_values()

        if not all_values:
            print("Sheet is empty!")
            return

        # Get headers
        headers = all_values[0]
        print(f"Current columns: {headers}")

        # Check if unique_id column already exists
        if "unique_id" in headers:
            col_index = headers.index("unique_id") + 1
            print(f"'unique_id' column already exists at column {col_index}")
        else:
            # Add header for unique_id
            col_index = len(headers) + 1
            sheet.update_cell(1, col_index, "unique_id")
            print(f"Added 'unique_id' header at column {col_index}")

        # Add unique IDs for each row using batch update
        num_rows = len(all_values)
        print(f"Processing {num_rows - 1} rows...")

        # Prepare batch update data
        updates = []
        unique_ids = []

        for row_idx in range(2, num_rows + 1):  # Start from row 2 (skip header)
            unique_id = create_unique_id()
            unique_ids.append(unique_id)
            updates.append([unique_id])

        # Batch update all rows at once
        start_cell = f"{chr(64 + col_index)}{2}"  # Convert column number to letter
        cell_range = f"{start_cell}:{chr(64 + col_index)}{num_rows}"
        sheet.batch_update([{"range": cell_range, "values": updates}])

        for idx, uid in enumerate(unique_ids, start=2):
            print(f"✓ Row {idx}: {uid}")

        print(f"\n✓ Successfully added unique IDs to {num_rows - 1} rows!")

    except gspread.exceptions.SpreadsheetNotFound:
        print(f"Error: Spreadsheet '{SPREADSHEET_NAME}' not found.")
        print("Make sure the spreadsheet exists and you have access to it.")
    except gspread.exceptions.WorksheetNotFound:
        print(f"Error: Sheet '{SHEET_NAME}' not found in the spreadsheet.")
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    add_unique_ids_to_sheet()
