import os
import json
from colorama import Fore, Style, init
from datetime import datetime

init(autoreset=True)

# Paths
order_folder = "/Users/aleonber20/Desktop/Leonberg Tech Services/data/client_orders"
db_folder = "/Users/aleonber20/Desktop/Leonberg Tech Services/data/client_database"
service_file = "/Users/aleonber20/Desktop/Leonberg Tech Services/data/parsed_services_2025.json"


def load_services(path):
    with open(path, "r") as f:
        return json.load(f)


def list_invoices():
    files = [f for f in os.listdir(order_folder) if f.endswith(".json")]
    if not files:
        print(Fore.RED + "❌ No invoices found.")
        return []

    print(Fore.CYAN + "\n📄 Available Invoices:")
    for idx, file in enumerate(files, 1):
        print(f"{idx}. {file.replace('_invoice.json', '').replace('_', ' ').title()}")
    return files


def select_invoice(files):
    selected = input(Fore.GREEN + "\nEnter the number of the invoice to edit: ").strip()
    if not selected.isdigit() or not (1 <= int(selected) <= len(files)):
        print(Fore.RED + "❌ Invalid selection.")
        return None
    return os.path.join(order_folder, files[int(selected) - 1])


def display_summary(data):
    print(Fore.MAGENTA + f"\n🧾 Invoice: {data['invoice_number']} | Date: {data['invoice_date']} | Status: {data.get('status', 'Unpaid')}")
    print("\nServices:")
    for s in data.get("services", []):
        print(f" - {s['service']} (${s['price']:.2f})")
    print("Products:")
    for p in data.get("products", []):
        print(f" - {p['name']} (${p['price']:.2f})")
    print(Fore.YELLOW + f"\nTotal: ${data['total']:.2f}")


def add_services(data):
    services = load_services(service_file)
    print("\n=== Add New Services ===")
    for idx, item in enumerate(services, 1):
        print(f"{idx}. {item['service']} — ${item['price']:.2f} ({item['category']})")

    selected = input("Enter service number(s) separated by commas: ").split(",")
    for s in selected:
        s = s.strip()
        if s.isdigit() and 1 <= int(s) <= len(services):
            data["services"].append(services[int(s) - 1])
            print(Fore.GREEN + f"✅ Added: {services[int(s) - 1]['service']}")


def add_products(data):
    print("\n=== Add Products ===")
    while True:
        name = input("Enter product name (or press Enter to stop): ").strip()
        if not name:
            break
        try:
            price = float(input(f"Enter price for '{name}': $"))
            data["products"].append({"name": name, "price": price})
            print(Fore.GREEN + f"✅ Added: {name} (${price:.2f})")
        except ValueError:
            print(Fore.RED + "❌ Invalid price.")


def update_totals(data):
    s_total = sum(i['price'] for i in data['services'])
    p_total = sum(i['price'] for i in data['products'])
    tax = round(p_total * 0.06, 2)
    total = round(s_total + p_total + tax, 2)

    data['service_subtotal'] = s_total
    data['product_subtotal'] = p_total
    data['tax'] = tax
    data['total'] = total


def update_status(data):
    current = data.get("status", "Unpaid")
    print(f"\nCurrent status: {current}")
    new_status = input("Set status to 'Paid' or 'Unpaid': ").strip().capitalize()
    if new_status in ["Paid", "Unpaid"]:
        data['status'] = new_status
        print(Fore.GREEN + f"✅ Status updated to {new_status}")

        if new_status == "Paid":
            os.makedirs(db_folder, exist_ok=True)
            client = data['client']
            profile_data = client.copy()
            profile_filename = f"{client['first_name']}_{client['last_name']}_profile.json".replace(" ", "_")
            profile_path = os.path.join(db_folder, profile_filename)
            with open(profile_path, "w") as f:
                json.dump(profile_data, f, indent=4)
            print(Fore.GREEN + f"📁 Client profile saved to database: {profile_path}")
    else:
        print(Fore.RED + "❌ Invalid status.")


def save_invoice(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)
    print(Fore.CYAN + f"📄 Invoice updated and saved to: {path}")


if __name__ == "__main__":
    invoices = list_invoices()
    if not invoices:
        exit()

    selected_path = select_invoice(invoices)
    if not selected_path:
        exit()

    with open(selected_path, "r") as f:
        invoice_data = json.load(f)

    display_summary(invoice_data)

    print("\n🔧 What would you like to do?")
    print("1. Add Services")
    print("2. Add Products")
    print("3. Change Status")
    print("4. Save and Exit")

    while True:
        action = input("Enter option number: ").strip()
        if action == "1":
            add_services(invoice_data)
        elif action == "2":
            add_products(invoice_data)
        elif action == "3":
            update_status(invoice_data)
        elif action == "4":
            update_totals(invoice_data)
            save_invoice(selected_path, invoice_data)
            break
        else:
            print("❌ Invalid choice.")
