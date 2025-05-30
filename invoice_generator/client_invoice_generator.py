# === Standard Library ===
import os, re, sys, json
from datetime import datetime
from collections import defaultdict

# === Third-Party ===
from colorama import init, Fore, Style

init(autoreset=True)



# === Local Modules ===
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from client_tools.service_loader import ServiceLoade, ServiceLoader

######################## GET CLIENTS FROM INTAKE FOLDER ########################

def list_intake_clients(intake_folder):
    print("\n📂 Checking for client intake files...")
    if not os.path.exists(intake_folder):
        print("❌ Intake folder does not exist.")
        return []
    files = [f for f in os.listdir(intake_folder) if f.endswith(".json")]
    if not files:
        print("⚠️ No intake files found.")
        return []
    print("\n📋 Available Clients (Intake Status):")
    for idx, file in enumerate(files, 1):
        print(f"{idx}. {file.replace('_intake.json', '').replace('_', ' ')}")
    return files

######################## GET LIST OF SERVICES ########################
loader = ServiceLoader()

# def load_services(path):
    # with open(path, "r") as f:
        # return json.load(f)
    
######################## FORMAT SETTINGS FOR SERVICE DISPLAY ########################

def format_service_display(services):
    grouped = defaultdict(list)
    for idx, item in enumerate(services, 1):
        grouped[item["category"]].append((idx, item))

    lines = []
    lines.append("╔════════════════════════════════════════════════════════════╗")
    lines.append("║                 === Available Services ===                 ║")
    lines.append("╚════════════════════════════════════════════════════════════╝\n")

    for category, items in grouped.items():
        box_width = 60
        title = f" {category} "
        border_top = f"╔{'═' * ((box_width - len(title)) // 2)}{title}{'═' * (box_width - len(title) - ((box_width - len(title)) // 2))}╗"
        lines.append(border_top)

        for idx, item in items:
            desc = item["service"]
            price = f"${item['price']:.2f}"
            dots = '.' * (box_width - len(desc) - len(price) - 8)
            line = f"║ {str(idx).rjust(2)}. {desc} {dots} {price} ║"
            lines.append(line)

        lines.append(f"╚{'═' * box_width}╝\n")

    return "\n".join(lines)

######################## PRINT SERVICE LIST MENU ########################

def display_services(services):
    print(format_service_display(services))

######################## SERVICE SELECTION ########################

def select_services(services):
    selected = []
    while True:
        entry = input("Enter service # to add (or press Enter to finish): ").strip()
        if not entry:
            break
        if not entry.isdigit() or not (1 <= int(entry) <= len(services)):
            print("❌ Invalid selection.")
            continue
        idx = int(entry) - 1
        selected.append(services[idx])
        print(f"✅ Added: {services[idx]['service']} — ${services[idx]['price']:.2f}")
    return selected

######################## ADD SELECTION TO ORDER ########################

def add_products():
    products = []
    print("\n=== Optional: Add Products (Taxable Items) ===")
    while True:
        name = input("Enter product name (or press Enter to finish): ").strip()
        if not name:
            break
        price = input(f"Enter price for '{name}': $").strip()
        try:
            price = float(price)
            products.append({"name": name, "price": price})
            print(f"✅ Added: {name} — ${price:.2f}")
        except ValueError:
            print("❌ Invalid price.")
    return products

######################## CALCULATE TOTAL ########################

def calculate_totals(services, products, tax_rate=0.06):
    service_total = sum(item['price'] for item in services)
    product_total = sum(item['price'] for item in products)
    tax = round(product_total * tax_rate, 2)
    total = round(service_total + product_total + tax, 2)
    return service_total, product_total, tax, total

######################## GENERATE INVOICE NUMBER ########################
def peek_invoice_number():
    counter_path = "/Users/aleonber20/Desktop/Leonberg Tech Services/.system/invoice_counter.txt"
    if not os.path.exists(counter_path):
        return 0
    with open(counter_path, "r") as f:
        return int(f.read().strip())

def increment_invoice_number():
    counter_path = "/Users/aleonber20/Desktop/Leonberg Tech Services/.system/invoice_counter.txt"
    current = peek_invoice_number()
    with open(counter_path, "w") as f:
        f.write(str(current + 1))

######################## INVOICE SUMMARY ########################
def strip_ansi(text):
    ansi_escape = re.compile(r'\x1b\[[0-9;]*m')
    return ansi_escape.sub('', text)

def generate_title_bar(title, width, color=Fore.MAGENTA):
        title_len = len(title) + 2  # 1 space on each side
        side_len = (width - title_len) // 2
        rem = (width - title_len) % 2
        return f"{color}╔{'═' * side_len} {title} {'═' * (side_len + rem)}╗"

def print_invoice_summary(services, products, s_total, p_total, tax, final_total):
    from colorama import Fore, Style

    box_width = 80
    label_width = 60  # width reserved for the label
    value_width = box_width - label_width - 6  # for price and spacing

    top_border = generate_title_bar("INVOICE SUMMARY", box_width)
    divider = f"{Fore.MAGENTA}╠{'═' * box_width}╣"
    bottom_border = f"{Fore.MAGENTA}╚{'═' * box_width}╝"

    print("\n" + top_border)

    def padded_line(label, value, color=Fore.CYAN):
        label = f"{label[:label_width]}".ljust(label_width)
        value = f"{value:>{value_width}}"
        inner = f"  {color}{label}{value}  "
        padding = box_width - len(strip_ansi(inner))
        return f"{Fore.MAGENTA}║{inner}{' ' * padding}{Fore.MAGENTA}║"


    for s in services:
        print(padded_line(s["service"], f"${s['price']:.2f}", Fore.CYAN))

    for p in products:
        print(padded_line(p["name"] + " (Product)", f"${p['price']:.2f}", Fore.CYAN))

    print(divider)
    print(padded_line("Services Subtotal:", f"${s_total:.2f}", Fore.YELLOW))
    print(padded_line("Products Subtotal:", f"${p_total:.2f}", Fore.YELLOW))
    print(padded_line("Tax (6% on products):", f"${tax:.2f}", Fore.YELLOW))
    print(padded_line("TOTAL:", f"${final_total:.2f}", Fore.GREEN + Style.BRIGHT))
    print(bottom_border)


######################## MAIN LOGIC ########################

def main():
    intake_folder = "/Users/aleonber20/Desktop/Leonberg Tech Services/data/client_intake"
    service_file = "/Users/aleonber20/Desktop/Leonberg Tech Services/data/parsed_services_2025.json"

    print("=== Leonberg Tech Services — New Order Intake ===")
    print("1. New Customer – New Order")
    print("2. Past Customer – New Order")
    choice = input("Choose an option (1 or 2): ").strip()

    if choice == "2":
        # === Past Client New Order ===
        if len(sys.argv) > 1:
            profile_path = sys.argv[1]
            if not os.path.exists(profile_path):
                print(Fore.RED + f"❌ Profile file not found: {profile_path}")
                return
            with open(profile_path, "r") as f:
                client_data = json.load(f)
            print(Fore.GREEN + f"\n✅ Loaded past client profile for {client_data['first_name']} {client_data['last_name']}.")

        else:
            # Fallback — ask user to select from /Client Database/
            print(Fore.YELLOW + "\n⚠️ No profile passed from main hub. Searching Client Database manually...")
            client_db = "/Users/aleonber20/Desktop/Leonberg Tech Services/data/client_database"
            if not os.path.exists(client_db):
                print(Fore.RED + "❌ Client Database folder not found.")
                return
            files = [f for f in os.listdir(client_db) if f.endswith("_profile.json")]
            if not files:
                print(Fore.YELLOW + "⚠️ No client profiles found.")
                return

            print(Fore.CYAN + "\n📋 Available Clients:")
            for idx, file in enumerate(files, 1):
                print(f"{idx}. {file.replace('_profile.json', '').replace('_', ' ').title()}")

            selected = input(Fore.GREEN + "\nEnter the number of the client to continue: ").strip()
            if not selected.isdigit() or not (1 <= int(selected) <= len(files)):
                print(Fore.RED + "❌ Invalid selection.")
                return

            profile_path = os.path.join(client_db, files[int(selected) - 1])
            with open(profile_path, "r") as f:
                client_data = json.load(f)
            print(Fore.GREEN + f"\n✅ Loaded client: {client_data['first_name']} {client_data['last_name']}.")

    elif choice == "1":
        client_files = list_intake_clients(intake_folder)
        if not client_files:
            return
        selected = input("\nEnter the number for the client intake to continue: ").strip()
        if not selected.isdigit() or int(selected) < 1 or int(selected) > len(client_files):
            print("❌ Invalid selection.")
            return
        
        selected_file = client_files[int(selected) - 1]
        full_path = os.path.join(intake_folder, selected_file)
        with open(full_path, "r") as f:
            client_data = json.load(f)
        
        print(f"\n✅ Loaded intake file for {client_data['first_name']} {client_data['last_name']}.")

        # Load services and begin service selection
        services = loader.get_all_services()
        display_services(services)
        selected_services = select_services(services)
        products = add_products()

        s_total, p_total, tax, final_total = calculate_totals(selected_services, products)

        # Ask user if invoice is paid
        while True:
            status_input = input("💳 Is this invoice paid? (yes/no): ").strip().lower()
            if status_input in ["yes", "y"]:
                status = "Paid"
                break
            elif status_input in ["no", "n"]:
                status = "Unpaid"
                break
            else:
                print("❌ Please enter 'yes' or 'no'.")

        invoice_number = f"INV-{peek_invoice_number():05d}"
        invoice_date = datetime.today().strftime("%B %d, %Y")

        # Print invoice summary
        print_invoice_summary(selected_services, products, s_total, p_total, tax, final_total)
        info_box_width = 70
        invoice_line = f"{Fore.LIGHTCYAN_EX}🧾  Invoice Number: {invoice_number}"
        date_line = f"{Fore.LIGHTCYAN_EX}📅  Date: {invoice_date}"
        status_line = f"{Fore.LIGHTCYAN_EX}💼  Status: {status}"

        # Center-align lines within box
        top_border = f"{Fore.MAGENTA}╔{'═' * info_box_width}╗"
        bottom_border = f"{Fore.MAGENTA}╚{'═' * info_box_width}╝"
        line1 = f"{Fore.MAGENTA}║ {invoice_line.ljust(info_box_width - 2)} ║"
        line2 = f"{Fore.MAGENTA}║ {date_line.ljust(info_box_width - 2)} ║"
        line3 = f"{Fore.MAGENTA}║ {status_line.ljust(info_box_width - 2)} ║"

        print("\n" + top_border)
        print(line1)
        print(line2)
        print(line3)
        print(bottom_border + "\n")

        invoice_data = {
            "client": {
                "name": f"{client_data['first_name']} {client_data['last_name']}",
                "contact": {
                    "mobile": client_data.get("mobile_phone", ""),
                    "home": client_data.get("home_phone", ""),
                    "email": client_data.get("email", "")
                },
                "intake_date": client_data.get("intake_date", ""),
                "address": client_data.get("address", "")
            },
            "invoice_number": invoice_number,
            "invoice_date": invoice_date,
            "services": selected_services,
            "products": products,
            "service_subtotal": s_total,
            "product_subtotal": p_total,
            "tax": tax,
            "client": client_data,  # if this variable holds the intake details
            "total": final_total,
            "status": status
        }

        save_path = "/Users/aleonber20/Desktop/Leonberg Tech Services/data/client_orders"
        os.makedirs(save_path, exist_ok=True)
        safe_filename = f"{client_data['first_name']}_{client_data['last_name']}_{invoice_number}.json".replace(" ", "_")

        filename = os.path.join(save_path, safe_filename)
        with open(filename, "w") as f:
            json.dump(invoice_data, f, indent=4)
        print(f"📄 Invoice saved to: {filename}")

        # Save client profile to database if invoice is paid
        if status == "Paid":
            db_folder = "/Users/aleonber20/Desktop/Leonberg Tech Services/data/client_database"
            os.makedirs(db_folder, exist_ok=True)

            profile_data = client_data.copy()
            profile_filename = f"{client_data['first_name']}_{client_data['last_name']}_profile.json".replace(" ", "_")
            profile_path = os.path.join(db_folder, profile_filename)

            with open(profile_path, "w") as f:
                json.dump(profile_data, f, indent=4)

            print(Fore.GREEN + f"📁 Client profile saved to database: {profile_path}")


        increment_invoice_number()

    else:
        print("❌ Invalid choice. Please select 1 or 2.")

if __name__ == "__main__":
    main()
