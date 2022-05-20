from django.test import TestCase
from django.test.client import Client
from django.shortcuts import reverse
from django.contrib.auth import get_user_model

from administration.invoice.models import Invoice, InvoiceItem
from administration.product_receipt.models import ProductReceipt, ProductReceiptItem
from administration.sales_order.models import SalesOrder
from webshop.product.models import Product

User = get_user_model()

# Income test

class IncomeViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        User.objects.create_user(
            username='customer',
            email='customer@test.com',
            password='customer'
        )
        User.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='admin'
        )
    
    @classmethod
    def setUpTestData(cls):
        sales_order = SalesOrder.objects.create(
            payment_type='cash',
            delivery_mode='delivery',
            net_price=100000,
            gross_price=127000,
            zip_code='2440',
            city='Százhalombatta',
            street_name='Valami utca',
            original_customer_name='Hegyi Dávid',
            customer_id=None,
            document_number_key=1,
            document_number='VME-1',
            status='in_progress'
        )
        Invoice.objects.create(
            payment_type='cash',
            delivery_mode='delivery',
            net_price=100000,
            gross_price=127000,
            zip_code='2440',
            city='Százhalombatta',
            street_name='Valami utca',
            original_customer_name='Hegyi Dávid',
            customer_id=None,
            account_number_key=1,
            account_number='SZA-1',
            status='in_progress',
            debt=127000,
            conn_sales_order_id=sales_order
        )
        Invoice.objects.create(
            payment_type='cash',
            delivery_mode='delivery',
            net_price=200000,
            gross_price=254000,
            zip_code='2440',
            city='Százhalombatta',
            street_name='Valami utca',
            original_customer_name='Hegyi Dávid',
            customer_id=None,
            account_number_key=2,
            account_number='SZA-2',
            status='completed',
            debt=0,
            conn_sales_order_id=sales_order
        )
        Invoice.objects.create(
            payment_type='cash',
            delivery_mode='delivery',
            net_price=100000,
            gross_price=118000,
            zip_code='2440',
            city='Százhalombatta',
            street_name='Valami utca',
            original_customer_name='Hegyi Dávid',
            customer_id=None,
            account_number_key=3,
            account_number='SZA-3',
            status='completed',
            debt=0,
            conn_sales_order_id=sales_order
        )

    def test_get_income_list_with_superuser(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('admin_core:je78jy_query:income-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(u"VME-1" in response.content.decode('utf8'))
        self.assertFalse(u"SZA-1" in response.content.decode('utf8'))
        self.assertTrue(u"SZA-2" in response.content.decode('utf8'))
        self.assertTrue(u"SZA-3" in response.content.decode('utf8'))
        self.assertTrue(u"Bevételek" in response.content.decode('utf8'))
        self.assertTrue(u"Összes nettó bevétel: 3000 Ft" in response.content.decode('utf8'))
        self.assertTrue(u"Összes bruttó bevétel: 3720 Ft" in response.content.decode('utf8'))

    def test_get_income_list_without_superuser(self):
        # Bejelentkezés nélkül
        response = self.client.get(reverse('admin_core:je78jy_query:income-list'))
        self.assertEqual(response.status_code, 302)

        # Vásárló fiókkal bejelentkezve
        self.client.login(username='customer', password='customer')
        response = self.client.get(reverse('admin_core:je78jy_query:income-list'))
        self.assertEqual(response.status_code, 302)

# Stock movement test

class StockMovementViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        User.objects.create_user(
            username='customer',
            email='customer@test.com',
            password='customer'
        )
        User.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='admin'
        )
    
    @classmethod
    def setUpTestData(cls):
        product1 = Product.objects.create(
            name="Teszt termék1",
            net_price=10000,
            vat=27,
            free_stock=10,
            reserved_stock=0
        )
        product2 = Product.objects.create(
            name="Teszt termék2",
            net_price=10000,
            vat=27,
            free_stock=10,
            reserved_stock=0
        )
        sales_order = SalesOrder.objects.create(
            payment_type='cash',
            delivery_mode='delivery',
            net_price=100000,
            gross_price=127000,
            zip_code='2440',
            city='Százhalombatta',
            street_name='Valami utca',
            original_customer_name='Hegyi Dávid',
            customer_id=None,
            document_number_key=1,
            document_number='VME-1',
            status='in_progress'
        )
        invalid_invoice = Invoice.objects.create(
            payment_type='cash',
            delivery_mode='delivery',
            net_price=100000,
            gross_price=127000,
            zip_code='2440',
            city='Százhalombatta',
            street_name='Valami utca',
            original_customer_name='Hegyi Dávid',
            customer_id=None,
            account_number_key=1,
            account_number='SZA-1',
            status='in_progress',
            debt=127000,
            conn_sales_order_id=sales_order
        )
        valid_invoice = Invoice.objects.create(
            payment_type='cash',
            delivery_mode='delivery',
            net_price=200000,
            gross_price=254000,
            zip_code='2440',
            city='Százhalombatta',
            street_name='Valami utca',
            original_customer_name='Hegyi Dávid',
            customer_id=None,
            account_number_key=2,
            account_number='SZA-2',
            status='completed',
            debt=0,
            conn_sales_order_id=sales_order
        )
        InvoiceItem.objects.create(
            original_name='Teszt termék1',
            original_producer='Teszt gyártó',
            original_net_price=100000,
            original_vat=27,
            original_package_quantity=1,
            original_package_display='db',
            quantity=20,
            product_id=product1,
            package_type_id=None,
            invoice_id=valid_invoice
        )
        InvoiceItem.objects.create(
            original_name='Teszt termék2',
            original_producer='Teszt gyártó',
            original_net_price=100000,
            original_vat=27,
            original_package_quantity=4,
            original_package_display='karton',
            quantity=2,
            product_id=product2,
            package_type_id=None,
            invoice_id=valid_invoice
        )
        InvoiceItem.objects.create(
            original_name='Teszt termék1',
            original_producer='Teszt gyártó',
            original_net_price=100000,
            original_vat=27,
            original_package_quantity=4,
            original_package_display='karton',
            quantity=2,
            product_id=product1,
            package_type_id=None,
            invoice_id=invalid_invoice
        )
        valid_pr = ProductReceipt.objects.create(
            document_number_key=1,
            document_number='BEV-1',
            status='final',
            sum_quantity=10
        )
        invalid_pr = ProductReceipt.objects.create(
            document_number_key=2,
            document_number='BEV-2',
            status='in_progress',
            sum_quantity=10
        )
        ProductReceiptItem.objects.create(
            original_name='Teszt termék1',
            quantity=10,
            product_id=product1,
            product_receipt_id=valid_pr
        )
        ProductReceiptItem.objects.create(
            original_name='Teszt termék2',
            quantity=5,
            product_id=product2,
            product_receipt_id=valid_pr
        )
        ProductReceiptItem.objects.create(
            original_name='Teszt termék1',
            quantity=100,
            product_id=product1,
            product_receipt_id=invalid_pr
        )

    def test_get_stock_movement_list_with_superuser(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('admin_core:je78jy_query:stock-movement-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(u"Teszt termék1" in response.content.decode('utf8'))
        self.assertTrue(u"Teszt termék2" in response.content.decode('utf8'))
        self.assertTrue(u"20 db" in response.content.decode('utf8'))
        self.assertTrue(u"8 db" in response.content.decode('utf8'))
        self.assertTrue(u"5 db" in response.content.decode('utf8'))
        self.assertTrue(u"10 db" in response.content.decode('utf8'))
        self.assertTrue(u"Összes eladott termék: 28 db" in response.content.decode('utf8'))
        self.assertTrue(u"Összes bevételezett termék: 15 db" in response.content.decode('utf8'))

    def test_get_stock_movement_list_without_superuser(self):
        # Bejelentkezés nélkül
        response = self.client.get(reverse('admin_core:je78jy_query:stock-movement-list'))
        self.assertEqual(response.status_code, 302)

        # Vásárló fiókkal bejelentkezve
        self.client.login(username='customer', password='customer')
        response = self.client.get(reverse('admin_core:je78jy_query:stock-movement-list'))
        self.assertEqual(response.status_code, 302)