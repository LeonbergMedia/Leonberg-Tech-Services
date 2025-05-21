import os
import subprocess
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# Paths
base = "/Users/aleonber20/Desktop/Leonberg Tech Services"
forms = os.path.join(base, "forms")
invoices = os.path.join(base, "invoice_generator")
profiles = os.path.join(base, "data/print_ready_invoices")
editor = os.path.join(invoices, "invoice_editor.py")


def run_script(script_path, args=None):
    try:
        command = ["python3", script_path]
        if args:
            command.extend(args)
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(Fore.RED + f"❌ Error running {script_path}: {e}")


def menu():
    while True:
        print(Fore.CYAN + "\n=== Leonberg Tech Services — Main Dashboard ===\n")
        print(Fore.YELLOW + "1." + Style.RESET_ALL + " Create New Client Intake")
        print(Fore.YELLOW + "2." + Style.RESET_ALL + " Create New Order (From Intake)")
        print(Fore.YELLOW + "3." + Style.RESET_ALL + " Generate Invoice PDF (From Order)")
        print(Fore.YELLOW + "4." + Style.RESET_ALL + " Edit Existing Invoice")
        print(Fore.YELLOW + "5." + Style.RESET_ALL + " Client Lookup")
        print(Fore.YELLOW + "6." + Style.RESET_ALL + " Exit")
        

        choice = input(Fore.GREEN + "\nChoose an option: ").strip()

        if choice == "1":
            run_script(os.path.join(forms, "client_intake_form.py"))

        elif choice == "2":
            run_script(os.path.join(invoices, "client_invoice_generator.py"))

        elif choice == "3":
            run_script(os.path.join(invoices, "invoice_pdf_generator.py"))

        elif choice == "4":
            run_script(os.path.join(invoices, "invoice_editor.py"))
        
        elif choice == "5":
            run_script(os.path.join(base, "client_tools", "client_lookup.py"))
          
        elif choice == "6":
            print(Fore.CYAN + "\n👋 Exiting Leonberg Tech Dashboard. Have a great day!")
            break

        else:
            print(Fore.RED + "❌ Invalid choice. Please select a number 1–6.")


if __name__ == "__main__":
    menu()
