from datetime import datetime

from administration.sales_order import utils as sales_order_utils
from administration.delivery_note.models import DeliveryNote
from .models import Invoice, InvoiceItem
from administration.admin_product import utils as product_utils


def create_invoice(sales_order):
    invoice = Invoice()
    account_number_key = Invoice.objects.all().order_by('-account_number_key') # Ez azért jó, mert egyből van account number és nem fordulhat elő olyan, hogy létezik számla úgy, hogy még nincs account number key.
    
    if account_number_key:
        invoice.account_number_key = account_number_key[0].account_number_key + 1
    else:
        invoice.account_number_key = 1
    invoice.account_number = f"SZA-{invoice.account_number_key}"
    invoice.net_price = sales_order.net_price
    invoice.gross_price = sales_order.gross_price
    invoice.debt = sales_order.gross_price
    invoice.status = 'in_progress'
    invoice.payment_type = sales_order.payment_type
    invoice.delivery_mode = sales_order.delivery_mode
    invoice.conn_sales_order_id = sales_order
    invoice.customer_id = sales_order.customer_id
    invoice.billing_zip_code = sales_order.zip_code
    invoice.billing_city = sales_order.city
    invoice.billing_street_name = sales_order.street_name
    invoice.billing_house_number = sales_order.house_number
    invoice.save()

    sales_order_utils.set_sales_order_status_to_partially_completed(sales_order)
    create_invoice_items(invoice, sales_order_utils.get_sales_order_items(sales_order))

    # Amikor a megrendelés pillanatában ki lett fizetve az összeg:
    if invoice.payment_type == 'card':
        invoice_settlement(invoice, sales_order)

def create_invoice_items(invoice, sales_order_items):
    for item in sales_order_items:
        invoice_item = InvoiceItem()
        invoice_item.original_name = item.original_name
        invoice_item.original_producer = item.original_producer
        invoice_item.original_net_price = item.original_net_price
        invoice_item.original_vat = item.original_vat
        invoice_item.original_package_quantity = item.original_package_quantity
        invoice_item.original_package_display = item.original_package_display
        invoice_item.quantity = item.quantity
        invoice_item.product_id = item.product_id
        invoice_item.package_type_id = item.package_type_id
        invoice_item.invoice_id = invoice
        invoice_item.save()

def invoice_settlement(invoice, sales_order):
    invoice.status = 'completed'
    invoice.debt = 0
    invoice.settlement_date = datetime.now()
    invoice.save()

    # Termékek felszabadítása foglalt készletről.
    for item in invoice.items.all():
        product_utils.remove_stock(item.product_id, item.original_package_quantity*item.quantity)

    # VME státusz állítás.
    if sales_order.delivery_mode != 'personal':
        delivery_note = DeliveryNote.objects.filter(conn_sales_order_id=sales_order)
        
        if delivery_note.exists() and delivery_note[0].status == 'completed':
            sales_order_utils.set_sales_order_status_to_completed(sales_order)
    else:
        sales_order_utils.set_sales_order_status_to_completed(sales_order)