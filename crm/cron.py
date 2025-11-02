#["from gql.transport.requests import RequestsHTTPTransport", "from gql import", "gql", "Client"] 
#File: crm/cron.py
import datetime
from pathlib import Path
import requests

def log_crm_heartbeat():
    """
    Logs a timestamped 'CRM is alive' message every 5 minutes.
    Optionally checks the GraphQL endpoint to confirm responsiveness.
    """
    log_file = Path("/tmp/crm_heartbeat_log.txt")
    now = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")

    message = f"{now} CRM is alive"

    # Optional: Check GraphQL endpoint
    try:
        response = requests.post(
            "http://localhost:8000/graphql",
            json={"query": "{ hello }"},
            timeout=3
        )
        if response.status_code == 200:
            message += " | GraphQL OK"
        else:
            message += f" | GraphQL Error: {response.status_code}"
    except Exception as e:
        message += f" | GraphQL check failed: {e}"

    # Append to log file
    with log_file.open("a") as f:
        f.write(message + "\n")

    print(message)



def update_low_stock():
    """
    Calls the GraphQL mutation to restock low-stock products
    and logs results to /tmp/low_stock_updates_log.txt.
    """
    log_file = Path("/tmp/low_stock_updates_log.txt")
    graphql_url = "http://localhost:8000/graphql"

    # Define the GraphQL mutation
    mutation = """
    mutation {
      updateLowStockProducts {
        message
        updatedProducts {
          id
          name
          stock
        }
      }
    }
    """

    try:
        # Send POST request to GraphQL endpoint
        response = requests.post(graphql_url, json={"query": mutation})
        response.raise_for_status()
        data = response.json()

        # Extract data from the response
        update_info = data.get("data", {}).get("updateLowStockProducts", {})
        updated_products = update_info.get("updatedProducts", [])
        message = update_info.get("message", "No message returned")

        # Log results with timestamp
        timestamp = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
        with log_file.open("a") as f:
            f.write(f"\n[{timestamp}] {message}\n")
            for p in updated_products:
                f.write(f"  Product: {p['name']}, New Stock: {p['stock']}\n")

        print("Low-stock products updated successfully!")

    except Exception as e:
        timestamp = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
        with log_file.open("a") as f:
            f.write(f"\n[{timestamp}] Error: {e}\n")
        print(f"Error occurred: {e}")
