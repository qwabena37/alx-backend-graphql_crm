#!/bin/bash
## File: crm/cron_jobs/clean_inactive_customers.sh
## Navigate to the Django project root (adjust path if needed)
cd "$(dirname "$0")/../.."
#
PYTHON="/usr/bin/python3":
## Run the Django shell command to delete inactive customers
deleted_count=$(python3 manage.py shell <<EOF
from django.utils import timezone
from datetime import timedelta
from crm.models import Customer
#
one_year_ago = timezone.now() - timedelta(days=365)
inactive_customers = Customer.objects.filter(orders__isnull=True, date_joined__lt=one_year_ago)
count = inactive_customers.count()
inactive_customers.delete()
print(count)
EOF
)

## Log the result to /tmp with a timestamp
echo "$(date): Deleted ${deleted_count} inactive customers" >> /tmp/customer_cleanup_log.txt

