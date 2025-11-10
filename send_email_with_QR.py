import os
import smtplib
import time
from email import encoders
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import gspread
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials

# Load environment variables from .env.local
load_dotenv(".env.local")

# Setup Google Sheets authentication
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]
CREDENTIALS_FILE = "credentials.json"
SPREADSHEET_NAME = os.getenv("SPREADSHEET_NAME", "Your Spreadsheet Name")
SHEET_NAME = os.getenv("SHEET_NAME", "Sheet1")

# Email configuration
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# File paths
QR_CODES_DIR = os.getenv("QR_CODES_DIR", "qr_codes")
PDF_ATTACHMENT_PATH = os.getenv("PDF_ATTACHMENT_PATH", "event-schedule.pdf")
EMAIL_TEMPLATE_PATH = os.getenv("EMAIL_TEMPLATE_PATH", "email_template.html")

# Validate email configuration
if not SENDER_EMAIL or not SENDER_PASSWORD:
    raise ValueError("SENDER_EMAIL and SENDER_PASSWORD must be set in .env.local")


def authenticate_google_sheets():
    """Authenticate and return Google Sheets client"""
    creds = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=SCOPES)
    return gspread.authorize(creds)


def load_email_template(name):
    """Load email body from template file"""
    try:
        with open(EMAIL_TEMPLATE_PATH, "r", encoding="utf-8") as f:
            template = f.read()
            # Replace placeholder with actual name
            html_body = template.replace("{name}", name)
            return html_body
    except FileNotFoundError:
        print(f"Error: Email template file not found at {EMAIL_TEMPLATE_PATH}")
        # Return a basic template as fallback
        return f"<html><body><h1>Hello {name}</h1><p>Please find your QR code attached.</p></body></html>"


def send_email_with_qr_and_pdf(recipient_email, name, qr_image_path, pdf_path):
    """Send email with QR code image and PDF attachment"""
    try:
        # Create message
        msg = MIMEMultipart("related")
        msg["From"] = SENDER_EMAIL
        msg["To"] = recipient_email
        msg["Subject"] = os.getenv(
            "EMAIL_SUBJECT", "Event Confirmation - QR Code Attached"
        )

        # Create alternative part for HTML
        msg_alternative = MIMEMultipart("alternative")
        msg.attach(msg_alternative)

        # Attach HTML body from template
        html_body = load_email_template(name)
        msg_alternative.attach(MIMEText(html_body, "html"))

        # Attach QR code image
        if os.path.exists(qr_image_path):
            with open(qr_image_path, "rb") as attachment:
                img = MIMEImage(attachment.read(), name=os.path.basename(qr_image_path))
                img.add_header("Content-ID", "<qr_code>")
                img.add_header(
                    "Content-Disposition",
                    "inline",
                    filename=os.path.basename(qr_image_path),
                )
                msg.attach(img)
        else:
            print(f"Warning: QR code image not found: {qr_image_path}")

        # Attach PDF
        if os.path.exists(pdf_path):
            with open(pdf_path, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header(
                    "Content-Disposition",
                    f"attachment; filename= {os.path.basename(pdf_path)}",
                )
                msg.attach(part)
        else:
            print(f"Warning: PDF file not found: {pdf_path}")

        # Send email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)

        return True

    except Exception as e:
        print(f"Error sending email to {recipient_email}: {str(e)}")
        return False


def send_emails_with_qr_codes():
    """Send emails with QR codes to all recipients"""
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
        print(f"Columns: {headers}")

        # Find required columns
        required_cols = {"unique_id": None, "email": None, "name": None}
        for col_name in required_cols:
            if col_name in headers:
                required_cols[col_name] = headers.index(col_name)
            else:
                print(f"Error: '{col_name}' column not found!")
                return

        # Check if email_sent column exists, if not create it
        if "email_sent" not in headers:
            email_sent_col = len(headers) + 1
            sheet.update_cell(1, email_sent_col, "email_sent")
            print(f"Created 'email_sent' column at column {email_sent_col}")
        else:
            email_sent_col = headers.index("email_sent") + 1

        # Send emails
        print(f"\nSending emails...")
        sent_count = 0
        skipped_count = 0

        for row_idx in range(1, len(all_values)):  # Start from row 1 (skip header)
            row_data = all_values[row_idx]

            # Get email status
            email_sent_status = ""
            if email_sent_col - 1 < len(row_data):
                email_sent_status = row_data[email_sent_col - 1].strip().lower()

            # Skip if already sent
            if email_sent_status == "yes":
                print(f"⊘ Row {row_idx + 1}: Already sent, skipping...")
                skipped_count += 1
                continue

            # Get required data
            unique_id_col = required_cols["unique_id"]
            email_col = required_cols["email"]
            name_col = required_cols["name"]

            if (
                unique_id_col < len(row_data)
                and email_col < len(row_data)
                and name_col < len(row_data)
            ):
                unique_id = row_data[unique_id_col]
                recipient_email = row_data[email_col].strip()
                name = row_data[name_col]

                if unique_id and recipient_email:
                    # Find QR code image
                    qr_filename = f"qr_{unique_id[:8]}.png"
                    qr_path = os.path.join(QR_CODES_DIR, qr_filename)

                    # Send email
                    if send_email_with_qr_and_pdf(
                        recipient_email, name, qr_path, PDF_ATTACHMENT_PATH
                    ):
                        # Update sheet with status
                        sheet.update_cell(row_idx + 1, email_sent_col, "yes")
                        print(f"✓ Row {row_idx + 1}: Sent to {recipient_email}")
                        sent_count += 1
                    else:
                        print(
                            f"✗ Row {row_idx + 1}: Failed to send to {recipient_email}"
                        )

                    # Add 1 second delay to prevent spam marking
                    time.sleep(1)

        print(f"\n✓ Emails sent: {sent_count}")
        print(f"⊘ Emails skipped: {skipped_count}")

    except gspread.exceptions.SpreadsheetNotFound:
        print(f"Error: Spreadsheet '{SPREADSHEET_NAME}' not found.")
    except gspread.exceptions.WorksheetNotFound:
        print(f"Error: Sheet '{SHEET_NAME}' not found.")
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    send_emails_with_qr_codes()
