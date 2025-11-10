# QR Code Generator for Event Management

A comprehensive Python application for generating unique QR codes and sending them via email for event management. This system integrates with Google Sheets to manage participant data and automates the process of creating personalized QR codes for event attendees.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
  - [Terminal Interface (Recommended)](#terminal-interface-recommended)
  - [Manual Script Execution](#manual-script-execution)
- [Scripts Documentation](#scripts-documentation)
  - [main.py](#mainpy)
  - [generate_uniqueId.py](#generate_uniqueidpy)
  - [generate_QR.py](#generate_qrpy)
  - [send_email_with_QR.py](#send_email_with_qrpy)
- [File Structure](#file-structure)
- [Environment Variables](#environment-variables)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Overview

This QR Code Generator system is designed for event organizers who need to:
- Generate unique identifiers for event participants
- Create QR codes for each participant
- Send personalized emails with QR codes and event information
- Track email delivery status

The system uses Google Sheets as a database to store participant information and integrates with email services to automate communication.

## Features

- **🎯 Terminal Interface**: User-friendly command-line interface for easy navigation
- **📊 Google Sheets Integration**: Seamlessly connects with Google Sheets for data management
- **🆔 Unique ID Generation**: Creates UUID-based unique identifiers for each participant
- **📱 QR Code Generation**: Generates high-quality QR codes with customizable settings
- **📧 Email Automation**: Sends personalized HTML emails with embedded QR codes
- **⚡ Batch Processing**: Handles multiple participants efficiently
- **📈 Status Tracking**: Tracks email delivery status to prevent duplicates
- **🛡️ Error Handling**: Comprehensive error handling and logging
- **🎨 Customizable Templates**: Uses HTML templates for professional email formatting

## Project Structure

```
qr-code-gen/
├── main.py                  # Terminal interface (recommended entry point)
├── generate_uniqueId.py     # Script to generate unique IDs in Google Sheets
├── generate_QR.py          # Script to generate QR codes from unique IDs
├── send_email_with_QR.py   # Script to send emails with QR codes
├── setup.py                # Automated setup script
├── requirements.txt        # Python package dependencies
├── email_template.html     # HTML template for email content
├── env.example             # Environment configuration template
├── credentials.json        # Google Service Account credentials (not tracked)
├── .env.local             # Environment variables (not tracked)
├── .gitignore             # Git ignore file
├── qr_codes/              # Directory containing generated QR codes
├── event-logo.png         # Event logo
├── event-schedule.pdf     # Event schedule PDF
└── README.md              # This documentation file
```

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.7 or higher
- pip (Python package installer)
- A Google Cloud Platform account
- A Gmail account for sending emails

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/qr-code-gen.git
cd qr-code-gen
```

### 2. Install Dependencies

Using the requirements file (recommended):

```bash
pip install -r requirements.txt
```

### 3. Quick Setup (Optional)

Run the automated setup script:

```bash
python setup.py
```

This will automatically:
- Check Python version compatibility
- Install all required packages from `requirements.txt`
- Create necessary directories
- Set up environment configuration from template

### 4. Set Up Google Cloud Project

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google Sheets API and Google Drive API
4. Create a service account:
   - Go to IAM & Admin > Service Accounts
   - Click "Create Service Account"
   - Fill in the details and create
   - Download the JSON key file and rename it to `credentials.json`
   - Place it in the project root directory

### 5. Create Google Sheet

1. Create a new Google Sheet with the following columns:
   - `name`: Participant's name
   - `email`: Participant's email address
   - `unique_id`: Will be generated automatically
   - `email_sent`: Will be updated automatically
2. Share the sheet with the service account email (found in `credentials.json`)
3. Note the sheet name and worksheet name for configuration

## Configuration

### 1. Environment Variables

Copy the example environment file and configure it:

```bash
cp env.example .env.local
```

Edit `.env.local` with your actual values:

```env
# Google Sheets Configuration
SPREADSHEET_NAME=Event Participants Database
SHEET_NAME=Sheet1

# Email Configuration
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-gmail-app-password

# File Paths
QR_CODES_DIR=qr_codes
PDF_ATTACHMENT_PATH=event-schedule.pdf
EMAIL_TEMPLATE_PATH=email_template.html
EMAIL_SUBJECT=Event Confirmation - QR Code Attached
```

### 2. Gmail App Password

1. Enable 2-factor authentication on your Gmail account
2. Generate an App Password:
   - Go to Google Account settings
   - Security > 2-Step Verification > App passwords
   - Generate a new app password
   - Use this password in the `.env.local` file

### 3. Update Script Configuration

Edit the following variables in each script if needed:

**generate_uniqueId.py and generate_QR.py:**
```python
SPREADSHEET_NAME = "Event Participants Database"
SHEET_NAME = "Sheet1"
```

## Usage

### Terminal Interface (Recommended)

Run the interactive terminal interface for the best user experience:

```bash
python main.py
```

The terminal interface provides:

**Main Menu Options:**
1. **Generate Unique IDs** - Add unique identifiers to your Google Sheet
2. **Generate QR Codes** - Create QR code images from unique IDs
3. **Send Emails with QR Codes** - Send personalized emails to participants
4. **Run Complete Workflow** - Execute all steps in sequence
5. **Check Configuration** - Verify system setup and requirements
6. **View Project Status** - Display statistics and file information

**Features:**
- 🔍 **Configuration Checking**: Validates all prerequisites before execution
- ⚠️ **Safety Confirmations**: Multiple confirmations for email sending
- 📊 **Progress Tracking**: Real-time status updates during operations
- 🛡️ **Error Handling**: Comprehensive error detection and reporting
- 📈 **Statistics Display**: View QR code counts and file information

### Manual Script Execution

If you prefer to run scripts individually:

#### Step 1: Generate Unique IDs

```bash
python generate_uniqueId.py
```

**What it does:**
- Connects to your Google Sheet
- Checks if a `unique_id` column exists, creates it if not
- Generates UUID4-based unique identifiers for each participant
- Updates the sheet with the new unique IDs

#### Step 2: Generate QR Codes

```bash
python generate_QR.py
```

**What it does:**
- Reads unique IDs from the Google Sheet
- Generates QR codes containing the unique ID data
- Saves QR codes as PNG images in the `qr_codes/` directory
- Names files using the first 8 characters of the UUID

#### Step 3: Send Emails with QR Codes

```bash
python send_email_with_QR.py
```

**What it does:**
- Reads participant data from Google Sheet
- Checks email sending status to avoid duplicates
- Sends HTML emails with embedded QR codes and PDF attachments
- Updates the sheet with email delivery status

## Scripts Documentation

### main.py

**Purpose**: Interactive terminal interface for managing the entire QR code generation workflow.

**Key Features:**
- User-friendly menu system with numbered options
- Comprehensive configuration checking before each operation
- Safety confirmations for email sending operations
- Real-time progress tracking and status updates
- Complete workflow automation option
- Project statistics and file information display

**Usage:**
```bash
python main.py
```

**Menu Navigation:**
- Use number keys (0-6) to select options
- Follow on-screen prompts and confirmations
- Press Enter to continue after operations complete

### generate_uniqueId.py

**Purpose**: Generates unique UUID4-based identifiers for each participant in the Google Sheet.

**Key Functions:**
- `authenticate_google_sheets()`: Establishes connection with Google Sheets API
- `create_unique_id()`: Generates a UUID4 string
- `add_unique_ids_to_sheet()`: Main function that processes the sheet and adds unique IDs

**Configuration Options:**
- `SPREADSHEET_NAME`: Name of your Google Sheet
- `SHEET_NAME`: Name of the specific worksheet
- `CREDENTIALS_FILE`: Path to Google service account credentials

### generate_QR.py

**Purpose**: Creates QR codes from the unique IDs stored in the Google Sheet.

**Key Functions:**
- `authenticate_google_sheets()`: Google Sheets authentication
- `create_output_directory()`: Creates the output directory for QR codes
- `generate_qr_code(data, filename)`: Creates individual QR code images
- `generate_qr_codes_from_sheet()`: Main processing function

**QR Code Settings:**
- Version: 1 (automatic sizing)
- Error correction: Medium level
- Box size: 10 pixels per box
- Border: 2 boxes
- Colors: Black on white background

**Output:**
- PNG images saved in `qr_codes/` directory
- Filename format: `qr_{first_8_chars_of_uuid}.png`

### send_email_with_QR.py

**Purpose**: Sends personalized emails with QR codes and event information to participants.

**Key Functions:**
- `authenticate_google_sheets()`: Google Sheets connection
- `load_email_template(name)`: Loads and personalizes HTML email template
- `send_email_with_qr_and_pdf()`: Sends individual emails with attachments
- `send_emails_with_qr_codes()`: Main batch processing function

**Email Features:**
- HTML formatted emails using template
- Embedded QR code images
- PDF attachment (event schedule)
- Personalized content with participant names
- Professional email signature

## File Structure

### Core Files

- **credentials.json**: Google Service Account credentials (keep secure, not in version control)
- **.env.local**: Environment variables (not in version control)
- **email_template.html**: HTML template for email formatting
- **requirements.txt**: Python package dependencies

### Generated Files

- **qr_codes/**: Directory containing all generated QR code images
- **Individual QR files**: Named as `qr_{uuid_prefix}.png`

### Assets

- **event-logo.png**: Event logo for branding
- **event-schedule.pdf**: Event schedule attached to emails

## Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `SPREADSHEET_NAME` | Name of your Google Sheet | "Event Participants Database" |
| `SHEET_NAME` | Worksheet name | "Sheet1" |
| `SENDER_EMAIL` | Gmail address for sending emails | "event@gmail.com" |
| `SENDER_PASSWORD` | Gmail app password | "abcd efgh ijkl mnop" |
| `QR_CODES_DIR` | Directory for QR codes | "qr_codes" |
| `PDF_ATTACHMENT_PATH` | Path to PDF attachment | "event-schedule.pdf" |
| `EMAIL_TEMPLATE_PATH` | Path to email template | "email_template.html" |
| `EMAIL_SUBJECT` | Email subject line | "Event Confirmation - QR Code Attached" |

## Troubleshooting

### Common Issues

1. **Authentication Error**
   ```
   Error: [Errno 2] No such file or directory: 'credentials.json'
   ```
   **Solution**: Ensure `credentials.json` is in the project root directory.

2. **Spreadsheet Not Found**
   ```
   Error: Spreadsheet 'Event Participants Database' not found.
   ```
   **Solution**: Check the spreadsheet name and ensure the service account has access.

3. **Email Authentication Failed**
   ```
   Error: (535, b'5.7.8 Username and Password not accepted')
   ```
   **Solution**: Use Gmail App Password instead of regular password.

4. **QR Code Directory Missing**
   ```
   Warning: QR code image not found
   ```
   **Solution**: Run `Generate QR Codes` option before sending emails.

5. **Module Import Error**
   ```
   ModuleNotFoundError: No module named 'qrcode'
   ```
   **Solution**: Install dependencies with `pip install -r requirements.txt`

### Using the Terminal Interface for Troubleshooting

The terminal interface includes a **"Check Configuration"** option that will:
- Verify Python version compatibility
- Check for all required files
- Validate Python package installations
- Display directory and file status
- Provide specific guidance for fixing issues

### Debug Tips

- Use the terminal interface's configuration check feature
- Ensure all required columns exist in your Google Sheet
- Verify that the service account email has editor access to the sheet
- Check that the PDF attachment file exists
- Verify internet connectivity for API calls

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Getting Started Quickly:**

1. Clone the repository and install dependencies:
   ```bash
   git clone <repository-url>
   cd qr-code-gen
   pip install -r requirements.txt
   ```

2. Set up your Google credentials and configuration files

3. Run the terminal interface:
   ```bash
   python main.py
   ```

4. Use the **"Check Configuration"** option to verify everything is set up correctly

5. Follow the workflow: Generate IDs → Generate QR Codes → Send Emails

For detailed setup instructions, see the [Installation](#installation) and [Configuration](#configuration) sections above.