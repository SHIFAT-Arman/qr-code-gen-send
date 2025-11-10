#!/usr/bin/env python3
"""
QR Code Generator - Demo Script
Demonstrates basic usage of the QR code generation system.
"""

import os
import sys
from datetime import datetime


def print_demo_header():
    """Print demo header"""
    print("=" * 60)
    print("🎯 QR CODE GENERATOR - DEMO")
    print("=" * 60)
    print("📅 Demo Date:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("-" * 60)


def show_project_structure():
    """Display project structure"""
    print("\n📁 PROJECT STRUCTURE:")
    print("-" * 30)

    structure = [
        ("main.py", "Terminal interface (recommended)"),
        ("generate_uniqueId.py", "Generate unique IDs"),
        ("generate_QR.py", "Generate QR codes"),
        ("send_email_with_QR.py", "Send emails with QR codes"),
        ("requirements.txt", "Python dependencies"),
        ("env.example", "Environment configuration template"),
        ("email_template.html", "Email HTML template"),
        ("event-schedule.pdf", "Event schedule (example)"),
        ("event-logo.png", "Event logo (example)"),
        ("qr_codes/", "Generated QR code images"),
    ]

    for file_name, description in structure:
        status = "✅" if os.path.exists(file_name) else "❌"
        print(f"  {status} {file_name:<25} - {description}")


def show_workflow():
    """Display workflow steps"""
    print("\n🔄 WORKFLOW STEPS:")
    print("-" * 30)

    steps = [
        ("1. Setup", "Install dependencies and configure environment"),
        ("2. Google Sheets", "Prepare participant data (name, email columns)"),
        ("3. Generate IDs", "Add unique identifiers to each participant"),
        ("4. Generate QRs", "Create QR code images from unique IDs"),
        ("5. Send Emails", "Email QR codes to all participants"),
    ]

    for step, description in steps:
        print(f"  📍 {step:<15} - {description}")


def show_sample_data():
    """Display sample data structure"""
    print("\n📊 SAMPLE GOOGLE SHEET DATA:")
    print("-" * 40)
    print("| Name          | Email                  | unique_id      | email_sent |")
    print("|---------------|------------------------|----------------|------------|")
    print("| John Doe      | john@example.com       | abc123def456   | yes        |")
    print("| Jane Smith    | jane@example.com       | def456ghi789   | yes        |")
    print("| Bob Johnson   | bob@example.com        | ghi789jkl012   | no         |")
    print("\nNote: unique_id and email_sent columns are auto-generated")


def show_commands():
    """Display available commands"""
    print("\n⚡ AVAILABLE COMMANDS:")
    print("-" * 30)

    commands = [
        ("python main.py", "Launch terminal interface (recommended)"),
        ("python setup.py", "Run automated setup"),
        ("python generate_uniqueId.py", "Generate unique IDs only"),
        ("python generate_QR.py", "Generate QR codes only"),
        ("python send_email_with_QR.py", "Send emails only"),
        ("pip install -r requirements.txt", "Install dependencies"),
    ]

    for command, description in commands:
        print(f"  🔸 {command:<30} - {description}")


def show_configuration():
    """Display configuration requirements"""
    print("\n⚙️ CONFIGURATION REQUIRED:")
    print("-" * 35)

    configs = [
        ("credentials.json", "Google Service Account key file"),
        (".env.local", "Environment variables (from env.example)"),
        ("Google Sheet", "Shared with service account email"),
        ("Gmail App Password", "For email sending authentication"),
    ]

    for config, description in configs:
        print(f"  🔧 {config:<20} - {description}")


def show_quick_start():
    """Display quick start guide"""
    print("\n🚀 QUICK START GUIDE:")
    print("-" * 25)
    print("1. Clone repository and install dependencies:")
    print("   pip install -r requirements.txt")
    print()
    print("2. Set up Google Cloud credentials:")
    print("   - Create service account")
    print("   - Download credentials.json")
    print()
    print("3. Configure environment:")
    print("   cp env.example .env.local")
    print("   # Edit .env.local with your values")
    print()
    print("4. Prepare Google Sheet:")
    print("   - Add name and email columns")
    print("   - Share with service account")
    print()
    print("5. Run the application:")
    print("   python main.py")
    print()
    print("6. Follow terminal interface prompts!")


def check_demo_requirements():
    """Check what's available for demo"""
    print("\n🔍 DEMO ENVIRONMENT CHECK:")
    print("-" * 35)

    # Check Python version
    python_version = sys.version_info
    print(
        f"🐍 Python: {python_version.major}.{python_version.minor}.{python_version.micro}"
    )

    # Check key files
    files_to_check = [
        "main.py",
        "requirements.txt",
        "env.example",
        "email_template.html",
    ]

    for file in files_to_check:
        status = "✅ Found" if os.path.exists(file) else "❌ Missing"
        print(f"📄 {file:<20} - {status}")

    # Check directories
    dirs_to_check = ["qr_codes"]
    for directory in dirs_to_check:
        if os.path.exists(directory):
            file_count = len([f for f in os.listdir(directory) if f.endswith(".png")])
            print(f"📁 {directory:<20} - ✅ Found ({file_count} QR codes)")
        else:
            print(f"📁 {directory:<20} - ❌ Missing")


def main():
    """Main demo function"""
    print_demo_header()

    try:
        show_project_structure()
        show_workflow()
        show_sample_data()
        show_commands()
        show_configuration()
        check_demo_requirements()
        show_quick_start()

        print("\n" + "=" * 60)
        print("🎯 DEMO COMPLETE!")
        print("💡 Run 'python main.py' to start the application")
        print("📖 See README.md for detailed documentation")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ Demo error: {str(e)}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
