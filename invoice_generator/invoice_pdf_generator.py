import os
import json
from datetime import datetime
from reportlab.lib.pagesizes import LETTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from colorama import Fore, Style, init
init(autoreset=True)


def generate_invoice_pdf(json_path, output_folder):
    with open(json_path, 'r') as f:
        invoice_data = json.load(f)

    try:
        client_info = invoice_data['client']
        first = client_info.get("first_name", "")
        last = client_info.get("last_name", "")
        client_name = f"{first} {last}".strip() or "Unknown_Client"
    except KeyError:
        client_name = 'Unknown_Client'
    
    # ✅ Warn if client name was missing
    if client_name == 'Unknown_Client':
        print(Fore.YELLOW + "⚠️  Warning: Client name not found in invoice JSON.")

    # Build PDF filename
    filename_safe = f"{client_name.replace(' ', '_')}_invoice.pdf"

    client = invoice_data["client"]  # ✅ Keep this if you're using 'client' below
    filename_safe = f"{client_name.replace(' ', '_')}_invoice.pdf"  # ✅ Use this for safe filename

    output_path = os.path.join(output_folder, filename_safe)

    doc = SimpleDocTemplate(output_path, pagesize=LETTER, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=18)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='RightAlign', alignment=2, fontSize=10))
    styles.add(ParagraphStyle(name='InvoiceHeader', alignment=2, fontSize=14, textColor=colors.HexColor("#003366"), fontName="Helvetica-Bold"))
    elements = []

    # Header
    elements.append(Paragraph("<b>Leonberg Tech Services</b><br/>Professional Technical Support", styles["Normal"]))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("Invoice", styles["InvoiceHeader"]))
    elements.append(Spacer(1, 6))

    # Invoice Info
    invoice_info_data = [
        ["Date:", invoice_data.get("invoice_date", datetime.today().strftime("%B %d, %Y"))],
        ["Invoice #:", invoice_data.get("invoice_number", "INV-XXXXX")],
        ["Customer ID:", "LEON123"],
        ["Purchase Order #:", "—"],
        ["Payment Due by:", invoice_data.get("invoice_date", datetime.today().strftime("%B %d, %Y"))],
    ]
    info_table = Table(invoice_info_data, colWidths=[120, 200])
    info_table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("ALIGN", (1, 0), (-1, -1), "LEFT"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
    ]))
    elements.append(info_table)
    elements.append(Spacer(1, 10))

    # Bill To / Ship To
    addr = client.get("address", "").replace("\n", "<br/>")
    contact = client.get("contact", {})
    full_name = f"{client.get('first_name', '')} {client.get('last_name', '')}".strip() or "Client"
    client_block = f"<b>{full_name}</b><br/>{addr}<br/>Mobile: {contact.get('mobile', '')}<br/>Email: {contact.get('email', '')}"
    bill_ship_table = Table([
        [Paragraph("<b>Bill To:</b>", styles["Normal"]), Paragraph("<b>Ship To (If Different):</b>", styles["Normal"])],
        [Paragraph(client_block, styles["Normal"]), Paragraph(client_block, styles["Normal"])]
    ], colWidths=[270, 270])
    bill_ship_table.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.25, colors.black),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.grey),
    ]))
    elements.append(bill_ship_table)
    elements.append(Spacer(1, 14))

    # Services + Products Table
    items = [["Description", "Line Total"]]
    for s in invoice_data.get("services", []):
        items.append([s["service"], f"${s['price']:.2f}"])
    for p in invoice_data.get("products", []):
        items.append([p["name"] + " (Product)", f"${p['price']:.2f}"])
    item_table = Table(items, colWidths=[440, 100])
    item_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#003366")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 10),
        ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
        ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
    ]))
    elements.append(item_table)
    elements.append(Spacer(1, 10))

    # Notes
    notes = invoice_data.get("follow_up", "Thank you for your business!")
    elements.append(Table([[Paragraph("<b>Special Notes and Instructions</b>", styles["Normal"])]], colWidths=[540],
                          style=[("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#003366")),
                                 ("TEXTCOLOR", (0, 0), (-1, -1), colors.white),
                                 ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold")]))
    elements.append(Paragraph(notes, styles["Normal"]))
    elements.append(Spacer(1, 10))

    # Totals
    totals = invoice_data
    totals_table = Table([
        ["Services Subtotal:", f"${totals['service_subtotal']:.2f}"],
        ["Products Subtotal:", f"${totals['product_subtotal']:.2f}"],
        ["Tax (6% on products):", f"${totals['tax']:.2f}"],
        ["Total:", f"${totals['total']:.2f}"],
    ], colWidths=[440, 100])
    totals_table.setStyle(TableStyle([
        ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
        ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
        ("BACKGROUND", (0, -1), (-1, -1), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
    ]))
    elements.append(totals_table)
    elements.append(Spacer(1, 12))

    # Footer
    elements.append(Paragraph("Make all checks payable to Leonberg Tech Services", styles["Normal"]))
    elements.append(Spacer(1, 6))
    elements.append(Paragraph("<b>Thank you for your business!</b>", styles["Normal"]))
    elements.append(Spacer(1, 6))
    elements.append(Paragraph("Questions? Contact Alex Leonberg at +1 (267) 992-3679 or alex@leonbergtech.com", styles["Normal"]))

    doc.build(elements)
    print(f"✅ PDF saved to: {output_path}")

# === CLI Menu Logic ===

if __name__ == "__main__":
    intake_folder = "/Users/aleonber20/Desktop/Leonberg Tech Services/data/client_orders"
    output_folder = "/Users/aleonber20/Desktop/Leonberg Tech Services/data/print_ready_invoices"

    print("\n📄 Available Invoices:")
    files = [f for f in os.listdir(intake_folder) if f.endswith(".json")]
    if not files:
        print("❌ No invoice files found.")
        exit()

    for idx, file in enumerate(files, 1):
        print(f"{idx}. {file.replace('_invoice.json', '').replace('_', ' ').title()}")

    selected = input("\nEnter the number of the invoice to generate: ").strip()
    if not selected.isdigit() or int(selected) < 1 or int(selected) > len(files):
        print("❌ Invalid selection.")
        exit()

    chosen_file = files[int(selected) - 1]
    chosen_path = os.path.join(intake_folder, chosen_file)
    generate_invoice_pdf(chosen_path, output_folder)
