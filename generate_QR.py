import qrcode
import gspread
from google.oauth2.service_account import Credentials
import os

# Setup Google Sheets authentication
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]
CREDENTIALS_FILE = "credentials.json"
SPREADSHEET_NAME = "Spave8: Qr Codes"  # Change to your spreadsheet name
SHEET_NAME = "Sheet1"  # Change to your sheet name if different
OUTPUT_DIR = "qr_codes"  # Directory to save QR codes


def authenticate_google_sheets():
    """Authenticate and return Google Sheets client"""
    creds = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=SCOPES)
    return gspread.authorize(creds)


def create_output_directory():
    """Create output directory if it doesn't exist"""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"Created directory: {OUTPUT_DIR}")


def generate_qr_code(data, filename):
    """Generate QR code and save as image"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=2,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    filepath = os.path.join(OUTPUT_DIR, filename)
    img.save(filepath)
    return filepath


def generate_qr_codes_from_sheet():
    """Generate QR codes from unique_id column in Google Sheet"""
    try:
        # Create output directory
        create_output_directory()

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
        print(f"Columns: {headers}")

        # Find unique_id column
        if "unique_id" not in headers:
            print("Error: 'unique_id' column not found!")
            return

        unique_id_col = headers.index("unique_id")

        # Generate QR codes for each row
        print(f"\nGenerating QR codes...")
        count = 0

        for row_idx in range(1, len(all_values)):  # Start from row 1 (skip header)
            row_data = all_values[row_idx]

            if unique_id_col < len(row_data) and row_data[unique_id_col]:
                unique_id = row_data[unique_id_col]
                filename = f"qr_{unique_id[:8]}.png"  # Use first 8 chars of UUID

                generate_qr_code(unique_id, filename)
                print(f"✓ Generated: {filename}")
                count += 1

        print(
            f"\n✓ Successfully generated {count} QR codes in '{OUTPUT_DIR}' directory!"
        )

    except gspread.exceptions.SpreadsheetNotFound:
        print(f"Error: Spreadsheet '{SPREADSHEET_NAME}' not found.")
    except gspread.exceptions.WorksheetNotFound:
        print(f"Error: Sheet '{SHEET_NAME}' not found.")
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    generate_qr_codes_from_sheet()
