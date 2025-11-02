##!/bin/bash
#
## Define log file
LOG_FILE="/tmp/customer_cleanup_log.txt"

## Execute Django shell command to delete inactive customers
DELETED_COUNT=$(/usr/bin/python3 manage.py shell -c "
from django.utils import timezone
from datetime import timedelta
from crm.models import Customer
#
cutoff_date = timezone.now() - timedelta(days=365)
deleted, _ = Customer.objects.filter(last_order_date__lt=cutoff_date).delete()
print(deleted)
")

#Log the number of deleted customers with timestamp
echo \"$(date '+%Y-%m-%d %H:%M:%S') - Deleted customers: $DELETED_COUNT\" >> $LOG_FILE

