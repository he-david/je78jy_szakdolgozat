from django.db.models import Q

from administration.sales_order.models import SalesOrderItem
from administration.invoice.models import InvoiceItem
from administration.delivery_note.models import DeliveryNoteItem
from administration.product_receipt.models import ProductReceiptItem

def get_product_with_less_stock(cart):
    wrong_items = []
    cart_items = cart.items.all()
    processed_products = []
    
    for item in cart_items:
        same_items = cart.items.filter(product_id=item.product_id)
        item_full_quantity = 0

        if item.product_id not in processed_products:
            for same_item in same_items:
                item_full_quantity += same_item.get_full_quantity()
            if item.product_id.free_stock < item_full_quantity:
                wrong_items.append(item)
        processed_products.append(item.product_id)
    return wrong_items

def has_no_open_document(product):
    sales_order_count = SalesOrderItem.objects.filter(~Q(sales_order_id__status='completed'), product_id=product, sales_order_id__deleted=False).count()
    invoice_count = InvoiceItem.objects.filter(~Q(invoice_id__status='completed'), product_id=product, invoice_id__deleted=False).count()
    delivery_note_count = DeliveryNoteItem.objects.filter(~Q(delivery_note_id__status='completed'), product_id=product, delivery_note_id__deleted=False).count()
    product_receipt_count = ProductReceiptItem.objects.filter(~Q(product_receipt_id__status='final'), product_id=product).count()
    return sales_order_count == 0 and invoice_count == 0 and delivery_note_count == 0 and product_receipt_count == 0

def reserve_stock(product, quantity):
    product.free_stock -= quantity
    product.reserved_stock += quantity
    product.save()

def free_stock(product, quantity):
    product.reserved_stock -= quantity
    product.free_stock += quantity
    product.save()

def remove_stock(product, quantity):
    product.reserved_stock -= quantity
    product.save()

def recover_stock_to_free(product, quantity):
    product.free_stock += quantity
    product.save()

def recover_stock_to_reserved(product, quantity):
    product.reserved_stock += quantity
    product.save()

def get_positive_stock_movement_sum(product):
    return sum(ProductReceiptItem.objects.filter(product_receipt_id__status='final', product_id=product).values_list('quantity', flat=True))

def get_negative_stock_movement_sum(product):
    neg_stock_sum = 0
    items = InvoiceItem.objects.filter(invoice_id__status='completed', product_id=product)
    for item in items:
        neg_stock_sum += item.quantity * item.original_package_quantity
    return neg_stock_sum