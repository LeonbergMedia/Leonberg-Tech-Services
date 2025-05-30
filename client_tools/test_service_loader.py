from service_loader import ServiceLoader

loader = ServiceLoader()

# Print all categories
categories = set(s["category"] for s in loader.get_all_services())
print("Available Categories:", categories)

# Get Add-Ons
addons = loader.get_services_by_category("Additional Services")
for item in addons:
    print(f"{item['service']}: ${item['price']}")

# Get price of a specific service
print("Printer Setup costs:", loader.get_service_price("Printer Setup (Driver & Test Print)"))