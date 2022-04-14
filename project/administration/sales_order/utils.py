from webshop.core.models import Address
from .models import SalesOrder, SalesOrderItem
from administration.admin_product import utils as product_utils


def set_sales_order_status_to_partially_completed(sales_order):
    sales_order.status = 'partially_completed'
    sales_order.save()

def set_sales_order_status_to_completed(sales_order):
    sales_order.status = 'completed'
    sales_order.save()

def get_sales_order_items(sales_order):
    return SalesOrderItem.objects.filter(sales_order_id=sales_order.id)

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
        sales_order_item.original_net_price = item.product_id.net_price
        sales_order_item.original_vat = item.product_id.vat
        sales_order_item.original_package_quantity = item.package_type_id.quantity
        sales_order_item.original_package_display = item.package_type_id.display_name
        sales_order_item.quantity = item.quantity
        sales_order_item.product_id = item.product_id
        sales_order_item.package_type_id = item.package_type_id
        sales_order_item.sales_order_id = sales_order
        product_utils.reserve_stock(item.product_id, item.package_type_id.quantity*item.quantity)
        sales_order_item.save()