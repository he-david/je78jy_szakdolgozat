from administration.sales_order.models import SalesOrderItem
from .models import Invoice, InvoiceItem


def create_invoice(sales_order):
    invoice = Invoice()
    account_number_key = Invoice.objects.all().order_by("-account_number_key")
    
    if account_number_key:
        invoice.account_number_key = account_number_key[0].account_number_key + 1
    else:
        invoice.account_number_key = 1
    invoice.account_number = f"SZA-{invoice.account_number_key}"
    invoice.net_price = sales_order.net_price
    invoice.gross_price = sales_order.gross_price
    invoice.status = 'in_progress'
    invoice.payment_type = sales_order.payment_type
    invoice.conn_sales_order_id = sales_order
    invoice.customer_id = sales_order.customer_id
    invoice.billing_address_id = sales_order.shipping_address_id
    invoice.save()

    set_sales_order_status(sales_order)
    create_invoice_items(invoice, get_sales_order_items(sales_order))

def set_sales_order_status(sales_order):
    sales_order.status = 'partially_completed'
    sales_order.save()

def get_sales_order_items(sales_order):
    return SalesOrderItem.objects.filter(sales_order_id=sales_order.id)

def create_invoice_items(invoice, sales_order_items):
    for item in sales_order_items:
        invoice_item = InvoiceItem()
        invoice_item.original_name = item.original_name
        invoice_item.original_producer = item.original_producer
        invoice_item.original_net_price = item.original_net_price
        invoice_item.original_vat = item.original_vat
        invoice_item.quantity = item.quantity
        invoice_item.product_id = item.product_id
        invoice_item.package_type_id = item.package_type_id
        invoice_item.invoice_id = invoice
        invoice_item.save()
