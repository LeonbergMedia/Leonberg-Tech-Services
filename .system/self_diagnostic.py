import os
import json
import importlib.util
from datetime import datetime

# Log file location
log_path = os.path.join(os.path.dirname(__file__), "debug.log")

# Files and modules to check
checks = [
    ("client_tools/client_lookup.py", "file"),
    ("invoice_generator/invoice_editor.py", "file"),
    ("invoice_generator/invoice_pdf_generator.py", "file"),
    ("invoice_generator/client_invoice_generator.py", "file"),
    ("forms/client_intake_form.py", "file"),
    ("main_hub.py", "file"),
    ("data/parsed_services_2025.json", "json"),
    ("data/client_database/", "folder"),
    ("data/client_orders/", "folder"),
    ("data/print_ready_invoices/", "folder")
]

results = []
timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")

def log(msg):
    with open(log_path, "a") as log_file:
        log_file.write(f"{timestamp} {msg}\n")

def check_file(path):
    return os.path.isfile(path)

def check_folder(path):
    return os.path.isdir(path)

def check_json(path):
    try:
        with open(path, "r") as f:
            json.load(f)
        return True
    except Exception:
        return False

def run_checks():
    passed = 0
    failed = 0
    base = os.path.dirname(os.path.dirname(__file__))
    print("\nLeonberg Tech Services Self-Diagnostic Report\n" + "-" * 45)
    for rel_path, ctype in checks:
        full_path = os.path.join(base, rel_path)
        if ctype == "file" and check_file(full_path):
            print(f"[✔] {rel_path} exists")
            log(f"[PASS] {rel_path}")
            passed += 1
        elif ctype == "folder" and check_folder(full_path):
            print(f"[✔] {rel_path} exists")
            log(f"[PASS] {rel_path}")
            passed += 1
        elif ctype == "json" and check_json(full_path):
            print(f"[✔] {rel_path} is valid JSON")
            log(f"[PASS] {rel_path}")
            passed += 1
        else:
            print(f"[✘] {rel_path} failed")
            log(f"[FAIL] {rel_path}")
            failed += 1
    print("-" * 45)
    print(f"SUMMARY: {passed} passed, {failed} failed\n")
    log(f"SUMMARY: {passed} passed, {failed} failed\n")

if __name__ == "__main__":
    run_checks()
