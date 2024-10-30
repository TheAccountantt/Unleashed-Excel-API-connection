# Unleashed Excel API Connector

This Python script connects to the Unleashed Software API, fetches data, processes it, and saves it to CSV files. It supports fetching data from various endpoints like StockOnHand, SalesInvoices, and Products.

## Prerequisites

- Python 3.x
- `requests` library

You can install the `requests` library using pip:

```sh
pip install requests
```

## Setup

1. Clone the repository to your local machine:

```sh
git clone https://github.com/yourusername/unleashed-excel-api-connector.git
cd unleashed-excel-api-connector
```

2. Open the `Unleashed_Excel_API_Connector.py` file and replace the placeholders for `API_ID` and `API_KEY` with your actual Unleashed API

 credentials

:

```python
API_ID = 'your_api_id_here'
API_KEY = 'your_api_key_here'
```

3. Update the `endpoints` dictionary in the `main` function with the paths where you want to save the fetched data:

```python
endpoints = {
    "StockOnHand": r"path to save stock on hand data",
    "SalesInvoices": r"path to save sales invoices data",
    "Products": r"path to save products data",
}
```

## Usage

Run the script using Python:

```sh
python 

Unleashed_Excel_API_Connector.py


```

The script will fetch data from the specified endpoints, process it, and save it to the specified CSV files.

## Functions

### `generate_signature(api_key, query_string)`

Generates an HMAC signature for API authentication.

### `get_utc_time()`

Returns the current UTC time in the required format.

### `fetch_data(endpoint, page=1, page_size=200)`

Fetches data from the Unleashed API for the specified endpoint.

### `save_to_csv(data, filename)`

Saves the fetched data to a CSV file.

### `format_date(raw_date)`

Converts raw date format to `dd/mm/yyyy`.

### `process_invoice_data(invoice)`

Processes invoice data and returns a list of processed lines.

