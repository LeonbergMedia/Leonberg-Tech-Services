import json
from datetime import datetime
import re
from dateutil import parser  # install via: pip install python-dateutil
import os

def format_us_phone(number):
    digits = re.sub(r'\D', '', number)
    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    return number

def parse_intake_date(input_str):
    try:
        # Assume year is always 2025
        parsed_date = parser.parse(input_str + " 2025", fuzzy=True)
        return parsed_date.strftime('%B %d, %Y')  # Format: May 18, 2025
    except Exception:
        print("❌ Invalid date format. Please enter formats like '5/18', 'May 18', or '18 May'.")
        return None

def collect_client_data():
    print("=== Leonberg Tech Services — Client Intake Form ===")
    client = {}

    client['first_name'] = input("First Name: ").strip()
    client['last_name'] = input("Last Name: ").strip()

    mobile = input("Mobile Phone (or leave blank): ").strip()
    home = input("Home Phone (or leave blank): ").strip()
    client['mobile_phone'] = format_us_phone(mobile) if mobile else ""
    client['home_phone'] = format_us_phone(home) if home else ""

    client['email'] = input("Email Address: ").strip()
    client['contact_preference'] = input("Preferred Contact Method (email, text, phone call): ").strip()

    print("\n=== Address Information (US Shipping Format) ===")
    line1 = input("Line 1: Full Name / Title / Company: ").strip()
    line2 = input("Line 2: Street Address (apt/suite + directionals): ").strip()
    city = input("City: ").strip()
    state = input("State (2-letter): ").strip().upper()
    zip_code = input("ZIP Code (5-digit): ").strip()
    line3 = f"{city}, {state} {zip_code}"
    client['address'] = f"{line1}\n{line2}\n{line3}"

    today_str = datetime.today().strftime('%B %d, %Y')
    use_today = input(f"Use today's date for intake? ({today_str}) [Y/n]: ").strip().lower()
    if use_today in ('', 'y', 'yes'):
        client['intake_date'] = today_str
    else:
        while True:
            raw_input = input("Enter intake date (e.g., '5/18', 'May 18', '18 May'): ").strip()
            parsed = parse_intake_date(raw_input)
            if parsed:
                client['intake_date'] = parsed
                break

    # Save to JSON

    # Save to JSON in holding folder
    file_safe_name = f"{client['first_name']}_{client['last_name']}".replace(" ", "_")
    holding_folder = "/Users/aleonber20/Desktop/Leonberg Tech Services/data/client_intake"
    os.makedirs(holding_folder, exist_ok=True)  # Ensure folder exists

    filename = os.path.join(holding_folder, f"{file_safe_name}_intake.json")
    with open(filename, 'w') as f:
        json.dump(client, f, indent=4)

    print(f"✅ Client intake saved to: {filename}")
    print("⚠️ Reminder: This client is in intake status only and not yet an active customer.")
    return filename


if __name__ == "__main__":
    collect_client_data()