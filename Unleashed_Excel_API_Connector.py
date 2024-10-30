import requests
import csv
import hashlib
import hmac
import base64
from datetime import datetime, timezone
import json

# Unleashed API credentials
API_ID = 'your_api_id_here'
API_KEY = 'your_api_key_here'
BASE_URL = 'https://api.unleashedsoftware.com'

# Function to generate HMAC signature
def generate_signature(api_key, query_string):
    message = query_string.encode('utf-8')
    secret = api_key.encode('utf-8')
    signature = hmac.new(secret, message, hashlib.sha256).digest()
    return base64.b64encode(signature).decode()

# Function to get current UTC time in required format
def get_utc_time():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")

# Function to fetch data from Unleashed API
def fetch_data(endpoint, page=1, page_size=200):
    url = f"{BASE_URL}{endpoint}/{page}?pageSize={page_size}"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "api-auth-id": API_ID,
        "api-auth-signature": generate_signature(API_KEY, f"pageSize={page_size}")
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

# Function to save data to CSV
def save_to_csv(data, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        if data:
            writer.writerow(data[0].keys())
            for item in data:
                writer.writerow(item.values())

# Function to convert raw date format to dd/mm/yyyy
def format_date(raw_date):
    if raw_date:
        try:
            timestamp = int(raw_date.strip("/Date()").split("+")[0]) / 1000
            return datetime.fromtimestamp(timestamp).strftime("%d/%m/%Y")
        except ValueError:
            return ""
    return ""

# Function to process invoice data
def process_invoice_data(invoice):
    invoice_number = invoice.get("InvoiceNumber", "")
    completed_date = format_date(invoice.get("CompletedDate", ""))
    order_number = invoice.get("OrderNumber", "")
    order_date = format_date(invoice.get("OrderDate", ""))
    order_status = invoice.get("OrderStatus", "")
    customer_code = invoice.get("Customer", {}).get("CustomerCode", "")
    customer_name = invoice.get("Customer", {}).get("CustomerName", "")
    warehouse_name = invoice.get("Warehouse", {}).get("WarehouseName", "")

    processed_lines = []
    for line in invoice.get("SalesOrderLines", []):
        product = line.get("Product", {})
        line_data = {
            "InvoiceNumber": invoice_number,
            "CompletedDate": completed_date,
            "OrderNumber": order_number,
            "OrderDate": order_date,
            "OrderStatus": order_status,
            "CustomerCode": customer_code,
            "CustomerName": customer_name,
            "WarehouseName": warehouse_name,
            "ProductCode": product.get("ProductCode", ""),
            "ProductDescription": product.get("ProductDescription", ""),
            "DueDate": format_date(line.get("DueDate", "")),
            "OrderQuantity": line.get("OrderQuantity", 0),
            "UnitPrice": line.get("UnitPrice", 0.0),
            "DiscountRate": line.get("DiscountRate", 0.0),
            "BCUnitPrice": line.get("BCUnitPrice", 0.0),
            "BCLineTotal": line.get("BCLineTotal", 0.0),
            "AverageLandedPriceAtTimeOfSale": line.get("AverageLandedPriceAtTimeOfSale", 0.0)
        }
        processed_lines.append(line_data)
    return processed_lines

# Main logic to fetch and process data
def main():
    endpoints = {
        "StockOnHand": r"path to save stock on hand data",
        "SalesInvoices": r"path to save sales invoices data",
        "Products": r"path to save products data",
    }

    for endpoint, filename in endpoints.items():
        page = 1
        all_data = []
        while True:
            print(f"Fetching {endpoint}, page {page}...")
            data = fetch_data(f"/{endpoint}", page=page)
            if data and "Items" in data:
                if endpoint == "SalesInvoices":
                    for invoice in data["Items"]:
                        all_data.extend(process_invoice_data(invoice))
                else:
                    all_data.extend(data["Items"])
                if len(data["Items"]) < 200:
                    break
                page += 1
            else:
                break

        if all_data:
            save_to_csv(all_data, filename)
            print(f"Data from {endpoint} saved to {filename}")
        else:
            print(f"No data found for endpoint: {endpoint}")

if __name__ == "__main__":
    main()
