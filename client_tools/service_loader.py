import os
import json

class ServiceLoader:
    def __init__(self, json_path="data/parsed_services_2025.json"):
        base_dir = os.path.dirname(os.path.dirname(__file__))
        self.file_path = os.path.join(base_dir, json_path)
        self.services = []
        self.load_services()

    def load_services(self):
        try:
            with open(self.file_path, "r") as f:
                self.services = json.load(f)
        except Exception as e:
            print(f"[!] Failed to load services: {e}")
            self.services = []

    def get_all_services(self):
        return self.services

    def get_services_by_category(self, category):
        return [s for s in self.services if s["category"] == category]

    def get_service_names(self):
        return [s["service"] for s in self.services]

    def get_service_price(self, service_name):
        for s in self.services:
            if s["service"] == service_name:
                return s["price"]
        return None

    def validate_services(self):
        valid = True
        for s in self.services:
            if not isinstance(s.get("price"), (int, float)) or "service" not in s or "category" not in s:
                print(f"[!] Invalid entry: {s}")
                valid = False
        return valid