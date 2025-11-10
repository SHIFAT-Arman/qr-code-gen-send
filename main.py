#!/usr/bin/env python3
"""
QR Code Generator - Terminal Interface
A user-friendly terminal interface for managing QR code generation workflow.
"""

import os
import sys
import time
from pathlib import Path

# Import our modules
try:
    from generate_QR import generate_qr_codes_from_sheet
    from generate_uniqueId import add_unique_ids_to_sheet
    from send_email_with_QR import send_emails_with_qr_codes
except ImportError as e:
    print(f"❌ Error importing modules: {e}")
    print("Please ensure all script files are in the same directory.")
    sys.exit(1)


class QRCodeManager:
    """Main class for managing QR code generation workflow"""

    def __init__(self):
        self.menu_options = {
            "1": ("Generate Unique IDs", self.generate_unique_ids),
            "2": ("Generate QR Codes", self.generate_qr_codes),
            "3": ("Send Emails with QR Codes", self.send_emails),
            "4": ("Run Complete Workflow", self.run_complete_workflow),
            "5": ("Check Configuration", self.check_configuration),
            "6": ("View Project Status", self.view_status),
            "0": ("Exit", self.exit_program),
        }

    def clear_screen(self):
        """Clear the terminal screen"""
        os.system("cls" if os.name == "nt" else "clear")

    def print_header(self):
        """Print application header"""
        print("=" * 60)
        print("🎯 QR CODE GENERATOR - TERMINAL INTERFACE")
        print("=" * 60)
        print("📧 Event Management & Email Automation System")
        print("-" * 60)

    def print_menu(self):
        """Print main menu options"""
        print("\n🔧 SELECT AN OPTION:")
        print("-" * 30)
        for key, (description, _) in self.menu_options.items():
            if key == "0":
                print(f"\n{key}. {description}")
            else:
                print(f"{key}. {description}")
        print("-" * 30)

    def get_user_choice(self):
        """Get and validate user input"""
        while True:
            choice = input("\n➤ Enter your choice (0-6): ").strip()
            if choice in self.menu_options:
                return choice
            else:
                print("❌ Invalid choice! Please enter a number from 0-6.")

    def wait_for_enter(self):
        """Wait for user to press Enter"""
        input("\nPress Enter to continue...")

    def print_step_header(self, step_number, title):
        """Print step header"""
        print(f"\n{'=' * 50}")
        print(f"📍 STEP {step_number}: {title.upper()}")
        print(f"{'=' * 50}")

    def check_prerequisites(self, step):
        """Check if prerequisites are met for each step"""
        issues = []

        # Check credentials.json
        if not os.path.exists("credentials.json"):
            issues.append("❌ credentials.json file not found")

        # Check .env.local
        if not os.path.exists(".env.local"):
            issues.append("❌ .env.local file not found")

        # Check email template
        if step >= 3 and not os.path.exists("email_template.html"):
            issues.append("❌ email_template.html file not found")

        # Check qr_codes directory for email step
        if step >= 3 and not os.path.exists("qr_codes"):
            issues.append("❌ qr_codes directory not found")
        elif step >= 3 and not any(f.endswith(".png") for f in os.listdir("qr_codes")):
            issues.append("⚠️  No QR code images found in qr_codes directory")

        return issues

    def generate_unique_ids(self):
        """Execute unique ID generation"""
        self.print_step_header(1, "Generate Unique IDs")

        issues = self.check_prerequisites(1)
        if issues:
            print("⚠️  CONFIGURATION ISSUES DETECTED:")
            for issue in issues:
                print(f"   {issue}")

            if any("❌" in issue for issue in issues):
                print("\n❌ Cannot proceed. Please fix the issues above.")
                self.wait_for_enter()
                return

            proceed = input("\n⚠️  Some issues detected. Continue anyway? (y/N): ")
            if proceed.lower() != "y":
                return

        print("\n🔄 Starting unique ID generation...")
        print("📊 This will add unique identifiers to your Google Sheet.")

        confirm = input("\nProceed with unique ID generation? (y/N): ")
        if confirm.lower() != "y":
            print("❌ Operation cancelled.")
            self.wait_for_enter()
            return

        try:
            print("\n" + "=" * 40)
            add_unique_ids_to_sheet()
            print("=" * 40)
            print("\n✅ Unique ID generation completed successfully!")

        except Exception as e:
            print(f"\n❌ Error during unique ID generation: {str(e)}")
            print("💡 Please check your configuration and try again.")

        self.wait_for_enter()

    def generate_qr_codes(self):
        """Execute QR code generation"""
        self.print_step_header(2, "Generate QR Codes")

        issues = self.check_prerequisites(2)
        if issues:
            print("⚠️  CONFIGURATION ISSUES DETECTED:")
            for issue in issues:
                print(f"   {issue}")

            if any("❌" in issue for issue in issues):
                print("\n❌ Cannot proceed. Please fix the issues above.")
                self.wait_for_enter()
                return

        print("\n🔄 Starting QR code generation...")
        print(
            "📱 This will create QR code images from unique IDs in your Google Sheet."
        )

        confirm = input("\nProceed with QR code generation? (y/N): ")
        if confirm.lower() != "y":
            print("❌ Operation cancelled.")
            self.wait_for_enter()
            return

        try:
            print("\n" + "=" * 40)
            generate_qr_codes_from_sheet()
            print("=" * 40)
            print("\n✅ QR code generation completed successfully!")

        except Exception as e:
            print(f"\n❌ Error during QR code generation: {str(e)}")
            print("💡 Please check your configuration and try again.")

        self.wait_for_enter()

    def send_emails(self):
        """Execute email sending"""
        self.print_step_header(3, "Send Emails with QR Codes")

        issues = self.check_prerequisites(3)
        if issues:
            print("⚠️  CONFIGURATION ISSUES DETECTED:")
            for issue in issues:
                print(f"   {issue}")

            if any("❌" in issue for issue in issues):
                print("\n❌ Cannot proceed. Please fix the issues above.")
                self.wait_for_enter()
                return

            proceed = input("\n⚠️  Some issues detected. Continue anyway? (y/N): ")
            if proceed.lower() != "y":
                return

        print("\n🔄 Starting email sending process...")
        print("📧 This will send personalized emails with QR codes to participants.")
        print("⚠️  Note: This will actually send emails! Make sure you're ready.")

        confirm = input("\n🚨 Are you sure you want to send emails? (y/N): ")
        if confirm.lower() != "y":
            print("❌ Operation cancelled.")
            self.wait_for_enter()
            return

        final_confirm = input("✉️  Final confirmation - Type 'SEND' to proceed: ")
        if final_confirm != "SEND":
            print("❌ Operation cancelled.")
            self.wait_for_enter()
            return

        try:
            print("\n" + "=" * 40)
            send_emails_with_qr_codes()
            print("=" * 40)
            print("\n✅ Email sending completed successfully!")

        except Exception as e:
            print(f"\n❌ Error during email sending: {str(e)}")
            print("💡 Please check your email configuration and try again.")

        self.wait_for_enter()

    def run_complete_workflow(self):
        """Run the complete workflow in sequence"""
        self.print_step_header("ALL", "Complete Workflow")

        print("🔄 This will run all steps in sequence:")
        print("   1️⃣  Generate Unique IDs")
        print("   2️⃣  Generate QR Codes")
        print("   3️⃣  Send Emails with QR Codes")
        print("\n⚠️  Warning: This includes sending actual emails!")

        confirm = input("\nProceed with complete workflow? (y/N): ")
        if confirm.lower() != "y":
            print("❌ Complete workflow cancelled.")
            self.wait_for_enter()
            return

        # Step 1: Generate Unique IDs
        try:
            print("\n" + "🔵" * 20)
            print("STEP 1/3: Generating Unique IDs...")
            print("🔵" * 20)
            add_unique_ids_to_sheet()
            print("✅ Step 1 completed!")
            time.sleep(2)

        except Exception as e:
            print(f"❌ Step 1 failed: {str(e)}")
            self.wait_for_enter()
            return

        # Step 2: Generate QR Codes
        try:
            print("\n" + "🟡" * 20)
            print("STEP 2/3: Generating QR Codes...")
            print("🟡" * 20)
            generate_qr_codes_from_sheet()
            print("✅ Step 2 completed!")
            time.sleep(2)

        except Exception as e:
            print(f"❌ Step 2 failed: {str(e)}")
            self.wait_for_enter()
            return

        # Step 3: Send Emails
        try:
            print("\n" + "🟢" * 20)
            print("STEP 3/3: Sending Emails...")
            print("🟢" * 20)
            send_emails_with_qr_codes()
            print("✅ Step 3 completed!")

        except Exception as e:
            print(f"❌ Step 3 failed: {str(e)}")
            self.wait_for_enter()
            return

        print("\n" + "🎉" * 30)
        print("🎉 COMPLETE WORKFLOW FINISHED SUCCESSFULLY! 🎉")
        print("🎉" * 30)
        self.wait_for_enter()

    def check_configuration(self):
        """Check system configuration"""
        self.print_step_header("CONFIG", "Configuration Check")

        print("🔍 Checking system configuration...\n")

        # Check Python version
        python_version = sys.version_info
        print(
            f"🐍 Python Version: {python_version.major}.{python_version.minor}.{python_version.micro}"
        )
        if python_version >= (3, 7):
            print("   ✅ Python version is compatible")
        else:
            print("   ❌ Python 3.7+ required")

        print()

        # Check required files
        required_files = {
            "credentials.json": "Google Service Account credentials",
            ".env.local": "Environment configuration",
            "email_template.html": "Email HTML template",
            "generate_uniqueId.py": "Unique ID generation script",
            "generate_QR.py": "QR code generation script",
            "send_email_with_QR.py": "Email sending script",
        }

        print("📁 Required Files:")
        all_files_present = True
        for file_path, description in required_files.items():
            if os.path.exists(file_path):
                print(f"   ✅ {file_path} - {description}")
            else:
                print(f"   ❌ {file_path} - {description}")
                all_files_present = False

        print()

        # Check directories
        print("📂 Directories:")
        if os.path.exists("qr_codes"):
            qr_count = len([f for f in os.listdir("qr_codes") if f.endswith(".png")])
            print(f"   ✅ qr_codes/ - {qr_count} QR code images")
        else:
            print("   ⚠️  qr_codes/ - Directory will be created when needed")

        print()

        # Check Python packages
        print("📦 Python Packages:")
        packages = ["qrcode", "gspread", "google.auth", "dotenv", "PIL"]
        for package in packages:
            try:
                __import__(package)
                print(f"   ✅ {package}")
            except ImportError:
                print(
                    f"   ❌ {package} - Install with: pip install -r requirements.txt"
                )
                all_files_present = False

        print("\n" + "=" * 50)
        if all_files_present:
            print("🎯 Configuration Status: ✅ READY TO USE")
        else:
            print("⚠️  Configuration Status: ❌ NEEDS ATTENTION")
            print("💡 Please fix the issues above before proceeding.")

        self.wait_for_enter()

    def view_status(self):
        """View project status and statistics"""
        self.print_step_header("STATUS", "Project Status")

        print("📊 Project Statistics:\n")

        # QR Codes count
        if os.path.exists("qr_codes"):
            qr_files = [f for f in os.listdir("qr_codes") if f.endswith(".png")]
            print(f"📱 QR Codes Generated: {len(qr_files)}")
        else:
            print("📱 QR Codes Generated: 0 (directory not found)")

        # File sizes
        files_to_check = [
            ("credentials.json", "Google Credentials"),
            (".env.local", "Environment Config"),
            ("email_template.html", "Email Template"),
            ("event-schedule.pdf", "Event Schedule PDF"),
            ("event-logo.png", "Event Logo"),
        ]

        print("\n📋 File Information:")
        for file_path, description in files_to_check:
            if os.path.exists(file_path):
                size = os.path.getsize(file_path)
                if size > 1024:
                    size_str = f"{size / 1024:.1f} KB"
                else:
                    size_str = f"{size} bytes"
                print(f"   📄 {description}: {size_str}")
            else:
                print(f"   ❌ {description}: Not found")

        # Recent QR codes
        if os.path.exists("qr_codes") and len(qr_files) > 0:
            print(f"\n🆕 Recent QR Codes (last 5):")
            recent_files = sorted(
                qr_files,
                key=lambda x: os.path.getmtime(os.path.join("qr_codes", x)),
                reverse=True,
            )[:5]
            for file in recent_files:
                mod_time = os.path.getmtime(os.path.join("qr_codes", file))
                time_str = time.strftime("%Y-%m-%d %H:%M", time.localtime(mod_time))
                print(f"   🔸 {file} - {time_str}")

        print("\n" + "=" * 50)
        print("💡 Tip: Use 'Check Configuration' to verify system setup")

        self.wait_for_enter()

    def exit_program(self):
        """Exit the application"""
        print("\n👋 Thank you for using QR Code Generator!")
        print("🎯 Visit the documentation for more information.")
        sys.exit(0)

    def run(self):
        """Main application loop"""
        while True:
            self.clear_screen()
            self.print_header()
            self.print_menu()

            choice = self.get_user_choice()
            _, action = self.menu_options[choice]

            try:
                action()
            except KeyboardInterrupt:
                print("\n\n❌ Operation interrupted by user")
                self.wait_for_enter()
            except Exception as e:
                print(f"\n❌ Unexpected error: {str(e)}")
                print("💡 Please check the logs and try again.")
                self.wait_for_enter()


def main():
    """Entry point of the application"""
    try:
        manager = QRCodeManager()
        manager.run()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Fatal error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
