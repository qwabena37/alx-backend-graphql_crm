#!/usr/bin/env python3
# File: crm/cron_jobs/send_order_reminders.py

import datetime
import requests
import json
from pathlib import Path

# === Configuration ===
GRAPHQL_URL = "http://localhost:8000/graphql"
LOG_FILE = Path("/tmp/order_reminders_log.txt")

# === Compute date range for the last 7 days ===
#"from gql import", "gql", "Client"
#"alx-backend-graphql_crm/crm/cron_jobs/send_order_reminders.py"
today = datetime.date.today()
one_week_ago = today - datetime.timedelta(days=7)

# === GraphQL query to fetch pending orders ===
query = """
query {
  orders(filter: {orderDate_Gte: "%s"}) {
    id
    customer {
      email
    }
    orderDate
  }
}
""" % (one_week_ago.isoformat())

# === Execute GraphQL request ===
try:
    response = requests.post(GRAPHQL_URL, json={'query': query})
    response.raise_for_status()
    data = response.json()

    orders = data.get("data", {}).get("orders", [])
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # === Log each order ===
    with LOG_FILE.open("a") as log:
        log.write(f"\n[{timestamp}] Found {len(orders)} orders in the last week:\n")
        for order in orders:
            log.write(f"  Order ID: {order['id']}, Email: {order['customer']['email']}\n")

    print("Order reminders processed!")

except Exception as e:
    with LOG_FILE.open("a") as log:
        log.write(f"\n[{datetime.datetime.now()}] Error: {e}\n")
    print(f"Error occurred: {e}")
