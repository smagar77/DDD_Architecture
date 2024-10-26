import requests
import csv

# local:
BASE_URL = "http://127.0.0.1:8072"
# PROD
# BASE_URL = "https://dev.agreco.in"


# Local: 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhYWExMjVlNi1mZWM1LTQzY2UtODhlYi04OTE3MzljM2NhN2UiLCJleHAiOjE2NjgxNDgzMjh9.v7ZpvLH-HrpB-l8DNjVbP7uXuRZO7bHENRJakKAJBbU'
# Prod: 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhYWExMjVlNi1mZWM1LTQzY2UtODhlYi04OTE3MzljM2NhN2UiLCJleHAiOjE2NjgxNTI3MTd9.WFWUHh1wcfrvVllV8NNfMWKhaewavj98yjtv66P9orI'
request_header = {
    'Authorization': ''
}

with open("request_item_import_1.csv", 'r') as csv_data:
    reader = csv.DictReader(csv_data)
    row_number = 1
    for row in reader:
        fpo_id = row.get('fpo_id')
        farmer_id = row.get('farmer_id')
        data = {
          "farmer_id": farmer_id,
          "fpo_id": fpo_id,
          "product_item_uuid": row.get('product_item_uuid'),
          "unit": row.get('unit'),
          "quantity": row.get('quantity')
        }
        print(f"[{row_number}][{farmer_id}] Adding request")
        resp = requests.post(
            f"{BASE_URL}/request-items/farmer/{farmer_id}",
            headers=request_header,
            json=data,
        )

        if resp.status_code != 201:
            print(f"[{row_number}][{farmer_id}] Error: {resp.text} for Request: {data}")
        else:
            print(f"[{row_number}][{farmer_id}] Added")
