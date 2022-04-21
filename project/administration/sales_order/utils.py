from administration.delivery_note.models import DeliveryNote
from administration.invoice.models import Invoice
from webshop.core.models import Address
from .models import SalesOrder, SalesOrderItem
from administration.admin_product import utils as product_utils
from administration.invoice import utils as invoice_utils
from administration.delivery_note import utils as delivery_note_utils

def set_sales_order_status(sales_order):
    status = 'in_progress'
    if sales_order.has_invoice():
        invoice = Invoice.objects.get(conn_sales_order_id=sales_order.id, deleted=False)
        status = 'partially_completed'

        if invoice.status == 'completed' and sales_order.delivery_mode == 'personal':
            status = 'completed'
        elif invoice.status == 'completed' and sales_order.has_delivery_note():
            delivery_note = DeliveryNote.objects.get(conn_sales_order_id=sales_order.id, deleted=False)

            if delivery_note.status == 'completed':
                status = 'completed'
    if sales_order.has_delivery_note() and status == 'in_progress':
        status = 'partially_completed'
    sales_order.status = status
    sales_order.save()

def create_sales_order(form, cart):
    # Létrehozni a megrendelést és felvenni mindent
    sales_order = SalesOrder()
    document_number_key = SalesOrder.objects.all().order_by('-document_number_key') # Ez azért jó, mert egyből van account number és nem fordulhat elő olyan, hogy létezik számla úgy, hogy még nincs account number key.
    
    if document_number_key:
        sales_order.document_number_key = document_number_key[0].document_number_key + 1
    else:
        sales_order.document_number_key = 1
    sales_order.document_number = f"VME-{sales_order.document_number_key}"
    sales_order.status = 'in_progress'
    sales_order.payment_type = form.cleaned_data['payment_type']
    sales_order.delivery_mode = form.cleaned_data['delivery_mode']
    sales_order.net_price = cart.net_price
    sales_order.gross_price = cart.gross_price

    address = Address.objects.filter(customer_id=cart.customer_id).first()
    sales_order.zip_code = address.zip_code
    sales_order.city = address.city
    sales_order.street_name = address.street_name
    sales_order.house_number = address.house_number
    sales_order.original_customer_name = f"{cart.customer_id.first_name} {cart.customer_id.first_name}"
    sales_order.customer_id = cart.customer_id
    sales_order.save()
    # Létrehozni a megrendelés itemeket
    create_sales_order_items(sales_order, cart.items.all())
    # Törölni a kosár tartalmát és a kosár árait
    cart.delete()

def create_sales_order_items(sales_order, cart_items):
    for item in cart_items:
        sales_order_item = SalesOrderItem()
        sales_order_item.original_name = item.product_id.name
        sales_order_item.original_producer = item.product_id.producer
        sales_order_item.original_net_price = item.product_id.get_net_price()
        sales_order_item.original_vat = item.product_id.vat
        sales_order_item.original_package_quantity = item.package_type_id.quantity
        sales_order_item.original_package_display = item.package_type_id.display_name
        sales_order_item.quantity = item.quantity
        sales_order_item.product_id = item.product_id
        sales_order_item.package_type_id = item.package_type_id
        sales_order_item.sales_order_id = sales_order
        product_utils.reserve_stock(item.product_id, item.package_type_id.quantity*item.quantity)
        sales_order_item.save()

def delete_sales_order(sales_order):
    free_reserved_stock(sales_order.items.all())
    sales_order.delete()

def free_reserved_stock(sales_order_items):
    for item in sales_order_items:
        product_utils.free_stock(item.product_id, item.original_package_quantity*item.quantity)

def cancel_sales_order(sales_order):
    # Ha van teljesített számla, akkor az végzi a készletmozgást.
    need_stock_movement = True

    # Számla lemondása/törlése
    if sales_order.has_invoice():
        invoice = Invoice.objects.get(conn_sales_order_id=sales_order.id, deleted=False)

        if invoice.status == 'completed':
            invoice_utils.cancel_invoice(invoice, True)
            need_stock_movement = False
        elif invoice.status != 'in_progress':
            invoice_utils.cancel_invoice(invoice, True)
        else:
            invoice_utils.delete_invoice(invoice)

    # Szállítólevél lemondása/törlése
    if sales_order.has_delivery_note():
        delivery_note = DeliveryNote.objects.get(conn_sales_order_id=sales_order.id, deleted=False)

        if delivery_note.status != 'in_progress':
            delivery_note_utils.cancel_delivery_note(delivery_note)
        else:
            delivery_note_utils.delete_delivery_note(delivery_note)

    if need_stock_movement:
        free_reserved_stock(sales_order.items.all())
    
    sales_order.status = 'cancelled'
    sales_order.deleted = True
    sales_order.save()