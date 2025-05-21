import os
import json
from colorama import Fore, Style, init
init(autoreset=True)

client_database_folder = "/Users/aleonber20/Desktop/Leonberg Tech Services/data/client_database"
client_orders_folder = "/Users/aleonber20/Desktop/Leonberg Tech Services/data/client_orders"

def list_clients():
    profiles = [f for f in os.listdir(client_database_folder) if f.endswith("_profile.json")]
    if not profiles:
        print(Fore.RED + "❌ No clients found in the database.")
        return None
    print(Fore.CYAN + "\n📋 Available Clients:")
    for i, file in enumerate(profiles, 1):
        name = file.replace("_profile.json", "").replace("_", " ").title()
        print(f"{i}. {name}")
    return profiles

def display_profile(profile_path):
    with open(profile_path, "r") as f:
        client = json.load(f)

    # Match orders
    first = client.get("first_name", "").lower()
    last = client.get("last_name", "").lower()
    orders = [f for f in os.listdir(client_orders_folder)
              if f.lower().startswith(f"{first}_{last}_") and f.endswith(".json")]

    print(Fore.MAGENTA + f"\n=== CLIENT PROFILE — {client.get('first_name', '')} {client.get('last_name', '')} ===\n")

    print(Fore.YELLOW + "📇 Contact Information:")
    print(Fore.WHITE + f"• Mobile: {client.get('mobile_phone', '—')}")
    print(f"• Home: {client.get('home_phone', '—')}")
    print(f"• Email: {client.get('email', '—')}")
    print(f"• Preferred Contact: {client.get('contact_preference', '—')}")

    print(Fore.YELLOW + "\n🏠 Address:")
    print(Fore.WHITE + client.get("address", "—"))

    print(Fore.YELLOW + "\n📅 Intake Date:")
    print(Fore.WHITE + client.get("intake_date", "—"))

    print(Fore.YELLOW + "\n📁 Past Orders:")
    if orders:
        for o in orders:
            print(Fore.WHITE + f"• {o}")
    else:
        print(Fore.LIGHTBLACK_EX + "• None found")

if __name__ == "__main__":
    client_files = list_clients()
    if client_files:
        selected = input(Fore.GREEN + "\nEnter the number of the client to look up: ").strip()
        if selected.isdigit() and 1 <= int(selected) <= len(client_files):
            selected_file = os.path.join(client_database_folder, client_files[int(selected) - 1])
            display_profile(selected_file)
        else:
            print(Fore.RED + "❌ Invalid selection.")
