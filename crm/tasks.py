from celery import shared_task
from datetime import datetime
import logging
from graphene_django.views import GraphQLView
from django.test import RequestFactory

@shared_task
def generate_crm_report():
    # Step 1: Prepare GraphQL query
    query = '''
    {
        customersCount
        ordersCount
        totalRevenue
    }
    '''
    
    # Step 2: Simulate GraphQL request
    factory = RequestFactory()
    request = factory.post('/graphql', {'query': query})
    response = GraphQLView.as_view(graphiql=False)(request)
    data = response.data if hasattr(response, 'data') else {}
    
    # Extract data
    # "import requests"
    total_customers = data.get('data', {}).get('customersCount', 0)
    total_orders = data.get('data', {}).get('ordersCount', 0)
    total_revenue = data.get('data', {}).get('totalRevenue', 0)

    # Step 3: Log report
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp} - Report: {total_customers} customers, {total_orders} orders, {total_revenue} revenue\n"

    with open("/tmp/crm_report_log.txt", "a") as f:
        f.write(log_entry)
    
    logging.info(log_entry)
