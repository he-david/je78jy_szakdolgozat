from .models import ProductReceipt, ProductReceiptItem
from administration.admin_product import utils as product_utils

from datetime import datetime

def create_product_receipt():
    receipt = ProductReceipt()
    receipt.status = 'in_progress'
    receipt.save()
    return receipt

def create_product_receipt_item(receipt_item, receipt_id):
    receipt = ProductReceipt.objects.get(id=receipt_id)
    old_receipt_item = ProductReceiptItem.objects.filter(product_id=receipt_item.product_id, product_receipt_id=receipt)
    
    if old_receipt_item.exists():
        old_receipt_item = old_receipt_item.first()
        old_receipt_item.quantity += receipt_item.quantity
        old_receipt_item.save()
    else:
        receipt_item.original_name = receipt_item.product_id.name
        receipt_item.product_receipt_id = receipt
        receipt_item.save()

    change_product_receipt_sum_quantity(receipt, receipt_item.quantity)

def change_product_receipt_sum_quantity(receipt, quantity):
    receipt.sum_quantity += quantity
    receipt.save()

def finalize_product_receipt(receipt):
    document_number_key = ProductReceipt.objects.filter(status='final').order_by('-document_number_key')
    
    if document_number_key:
        receipt.document_number_key = document_number_key[0].document_number_key + 1
    else:
        receipt.document_number_key = 1
    receipt.document_number = f"BEV-{receipt.document_number_key}"
    receipt.finalization_date = datetime.now()
    receipt.status = 'final'
    receipt.save()
    receipt_items = ProductReceiptItem.objects.filter(product_receipt_id=receipt)

    for item in receipt_items:
        product_utils.modify_product_quantity(item.product_id, item.quantity)