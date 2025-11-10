#!/usr/bin/env python3
"""
QR Code Generator Setup Script
Helps users set up the project environment and dependencies.
"""

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


def print_header():
    """Print setup script header"""
    print("=" * 60)
    print("🎯 QR Code Generator Setup Script")
    print("=" * 60)
    print()


def check_python_version():
    """Check if Python version is compatible"""
    print("📋 Checking Python version...")
    if sys.version_info < (3, 7):
        print("❌ Error: Python 3.7 or higher is required!")
        print(f"   Current version: {sys.version}")
        sys.exit(1)
    print(f"✅ Python {sys.version.split()[0]} is compatible")
    print()


def install_dependencies():
    """Install required Python packages"""
    print("📦 Installing dependencies...")
    try:
        # Check if pip is available
        subprocess.check_call(
            [sys.executable, "-m", "pip", "--version"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        # Install packages from requirements.txt
        if os.path.exists("requirements.txt"):
            print("   Installing from requirements.txt...")
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]
            )
        else:
            # Install individual packages if requirements.txt doesn't exist
            packages = [
                "qrcode[pil]>=7.4.2",
                "gspread>=5.12.0",
                "google-auth>=2.23.4",
                "google-auth-oauthlib>=1.1.0",
                "google-auth-httplib2>=0.1.1",
                "python-dotenv>=1.0.0",
                "Pillow>=9.0.0",
                "requests>=2.28.0",
            ]
            print("   Installing individual packages...")
            for package in packages:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])

        print("✅ Dependencies installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print("❌ Error: pip not found. Please install pip first.")
        sys.exit(1)
    print()


def create_directories():
    """Create necessary directories"""
    print("📁 Creating directories...")
    directories = ["qr_codes"]

    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"   ✅ Created: {directory}/")
        else:
            print(f"   ⚠️  Already exists: {directory}/")
    print()


def setup_environment_file():
    """Create .env.local from template"""
    print("⚙️  Setting up environment configuration...")

    env_example = "env.example"
    env_file = ".env.local"

    if not os.path.exists(env_example):
        print("   ❌ env.example not found!")
        return False

    if os.path.exists(env_file):
        response = input("   .env.local already exists. Overwrite? (y/N): ")
        if response.lower() != "y":
            print("   ⚠️  Keeping existing .env.local")
            return True

    shutil.copy2(env_example, env_file)
    print(f"   ✅ Created {env_file} from template")
    print(f"   📝 Please edit {env_file} with your actual configuration")
    return True


def check_credentials():
    """Check for Google credentials file"""
    print("🔑 Checking for Google credentials...")

    credentials_file = "credentials.json"
    if os.path.exists(credentials_file):
        try:
            with open(credentials_file, "r") as f:
                creds = json.load(f)
                if "type" in creds and creds["type"] == "service_account":
                    print("   ✅ Valid service account credentials found")
                    return True
                else:
                    print("   ❌ Invalid credentials format")
                    return False
        except json.JSONDecodeError:
            print("   ❌ Invalid JSON in credentials file")
            return False
    else:
        print("   ❌ credentials.json not found")
        return False


def print_next_steps(has_credentials):
    """Print next steps for the user"""
    print("🚀 Setup Complete! Next Steps:")
    print("-" * 40)

    if not has_credentials:
        print("1. 📥 Download Google Service Account credentials:")
        print("   - Go to Google Cloud Console")
        print("   - Create/select a project")
        print("   - Enable Google Sheets API and Drive API")
        print("   - Create a Service Account")
        print("   - Download JSON key and save as 'credentials.json'")
        print()

    print("2. 📝 Configure your settings:")
    print("   - Edit .env.local with your actual values")
    print("   - Set your spreadsheet name and Gmail credentials")
    print("   - Generate Gmail App Password (not regular password)")
    print()

    print("3. 📊 Prepare your Google Sheet:")
    print("   - Create columns: name, email")
    print("   - Share sheet with service account email")
    print("   - Add participant data")
    print()

    print("4. ▶️  Run the application:")
    print("   python main.py                  # Terminal interface (recommended)")
    print("   python generate_uniqueId.py     # Generate unique IDs")
    print("   python generate_QR.py           # Generate QR codes")
    print("   python send_email_with_QR.py    # Send emails")
    print()

    print("📖 For detailed instructions, see README.md")
    print("=" * 60)


def main():
    """Main setup function"""
    print_header()

    # Change to script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    try:
        check_python_version()
        install_dependencies()
        create_directories()
        setup_environment_file()
        has_credentials = check_credentials()

        print()
        print_next_steps(has_credentials)

    except KeyboardInterrupt:
        print("\n\n❌ Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error during setup: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
