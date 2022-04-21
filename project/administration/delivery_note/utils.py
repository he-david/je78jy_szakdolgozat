from administration.invoice.models import Invoice
from administration.sales_order import utils as sales_order_utils
from .models import DeliveryNote, DeliveryNoteItem

from datetime import datetime

def create_delivery_note(sales_order):
    delivery_note = DeliveryNote()
    document_number_key = DeliveryNote.objects.all().order_by('-document_number_key')

    if document_number_key:
        delivery_note.document_number_key = document_number_key[0].document_number_key + 1
    else:
        delivery_note.document_number_key = 1
    delivery_note.document_number = f"SZL-{delivery_note.document_number_key}"
    delivery_note.net_price = sales_order.net_price
    delivery_note.gross_price = sales_order.gross_price
    delivery_note.status = 'in_progress'
    delivery_note.payment_type = sales_order.payment_type
    delivery_note.delivery_mode = sales_order.delivery_mode
    delivery_note.conn_sales_order_id = sales_order
    delivery_note.original_customer_name = sales_order.original_customer_name
    delivery_note.customer_id = sales_order.customer_id
    delivery_note.shipping_zip_code = sales_order.zip_code
    delivery_note.shipping_city = sales_order.city
    delivery_note.shipping_street_name = sales_order.street_name
    delivery_note.shipping_house_number = sales_order.house_number
    delivery_note.save()

    sales_order_utils.set_sales_order_status(sales_order)
    create_delivery_note_items(delivery_note, sales_order.items.all())

def create_delivery_note_items(delivery_note, sales_order_items):
    for item in sales_order_items:
        delivery_note_item = DeliveryNoteItem()
        delivery_note_item.original_name = item.original_name
        delivery_note_item.original_producer = item.original_producer
        delivery_note_item.original_net_price = item.original_net_price
        delivery_note_item.original_vat = item.original_vat
        delivery_note_item.original_package_quantity = item.original_package_quantity
        delivery_note_item.original_package_display = item.original_package_display
        delivery_note_item.quantity = item.quantity
        delivery_note_item.product_id = item.product_id
        delivery_note_item.package_type_id = item.package_type_id
        delivery_note_item.delivery_note_id = delivery_note
        delivery_note_item.save()

def delivery_note_completion(delivery_note, sales_order):
    delivery_note.status = 'completed'
    delivery_note.completion_date = datetime.now()
    delivery_note.save()
    sales_order_utils.set_sales_order_status(sales_order)

def delete_delivery_note(delivery_note):
    sales_order = delivery_note.conn_sales_order_id
    delivery_note.delete()
    sales_order_utils.set_sales_order_status(sales_order)

def cancel_delivery_note(delivery_note):
    delivery_note.status = 'cancelled'
    delivery_note.deleted = True
    delivery_note.save()
    sales_order_utils.set_sales_order_status(delivery_note.conn_sales_order_id)
