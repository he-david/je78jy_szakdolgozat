from .models import SalesOrderItem

def set_sales_order_status_to_partially_completed(sales_order):
    sales_order.status = 'partially_completed'
    sales_order.save()

def set_sales_order_status_to_completed(sales_order):
    sales_order.status = 'completed'
    sales_order.save()

def get_sales_order_items(sales_order):
    return SalesOrderItem.objects.filter(sales_order_id=sales_order.id)