# File: crm/cron.py
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
