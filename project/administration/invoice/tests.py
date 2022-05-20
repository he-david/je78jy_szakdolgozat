from django.test import TestCase
from django.test.client import Client
from django.shortcuts import reverse
from django.contrib.auth import get_user_model

from administration.invoice.models import Invoice, InvoiceItem
from administration.sales_order.models import SalesOrder
from webshop.product.models import PackageType, Product

User = get_user_model()

# Views tests

class ViewTest(TestCase):
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
            id=1,
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
        invoice = Invoice.objects.create(
            id=1,
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
        InvoiceItem.objects.create(
            id=1,
            original_name='Teszt termék',
            original_producer='Teszt gyártó',
            original_net_price=100000,
            original_vat=27,
            original_package_quantity=1,
            original_package_display='db',
            quantity=1,
            product_id=None,
            package_type_id=None,
            invoice_id=invoice
        )

    # ListView tests

    def test_get_invoice_list_with_superuser(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('admin_core:admin_invoice:invoice-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(u"SZA-1" in response.content.decode('utf8'))
        self.assertTrue(u"Folyamatban" in response.content.decode('utf8'))

    def test_get_invoice_list_without_superuser(self):
        # Bejelentkezés nélkül
        response = self.client.get(reverse('admin_core:admin_invoice:invoice-list'))
        self.assertEqual(response.status_code, 302)

        # Vásárló fiókkal bejelentkezve
        self.client.login(username='customer', password='customer')
        response = self.client.get(reverse('admin_core:admin_invoice:invoice-list'))
        self.assertEqual(response.status_code, 302)

    # DetailView tests

    def test_get_invoice_detail_with_superuser(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('admin_core:admin_invoice:invoice-detail', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Számla módosítás")
        self.assertContains(response, "Kiegyenlítés")

    def test_get_invoice_detail_with_customer(self):
        # Bejelentkezés nélkül
        response = self.client.get(reverse('admin_core:admin_invoice:invoice-detail', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 302)

        # Vásárló fiókkal bejelentkezve
        self.client.login(username='customer', password='customer')
        response = self.client.get(reverse('admin_core:admin_invoice:invoice-detail', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 302)

    def test_get_invoice_detail_404(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('admin_core:admin_invoice:invoice-detail', kwargs={'id': 5}))
        self.assertEqual(response.status_code, 404)

# Model tests

class InvoiceModelTest(TestCase):
    def test_invoice_model(self):
        sales_order = SalesOrder.objects.create(
            id=1,
            payment_type='cash',
            delivery_mode='delivery',
            net_price=100000,
            gross_price=127000,
            zip_code='2440',
            city='Százhalombatta',
            street_name='Valami utca',
            original_customer_name='Hegyi Dávid',
            customer_id=None,
            status='in_progress'
        )
        invoice = Invoice.objects.create(
            id=1,
            payment_type='cash',
            delivery_mode='delivery',
            net_price=100000,
            gross_price=127000,
            zip_code='2440',
            city='Százhalombatta',
            street_name='Valami utca',
            original_customer_name='Hegyi Dávid',
            customer_id=None,
            status='in_progress',
            debt=127000,
            conn_sales_order_id=sales_order
        )
        self.assertEqual(str(invoice), f"#{invoice.id}")
        invoice.account_number_key=1
        invoice.account_number='SZA-1'
        self.assertEqual(str(invoice), invoice.account_number)

        self.assertIn(str(invoice.id), invoice.get_absolute_url())
        self.assertNotIn('2', invoice.get_absolute_url())

        self.assertEqual(1000, invoice.get_net_price())
        self.assertEqual(1270, invoice.get_gross_price())

    def test_invoice_item_model(self):
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
            status='in_progress'
        )
        invoice = Invoice.objects.create(
            payment_type='cash',
            delivery_mode='delivery',
            net_price=100000,
            gross_price=127000,
            zip_code='2440',
            city='Százhalombatta',
            street_name='Valami utca',
            original_customer_name='Hegyi Dávid',
            customer_id=None,
            status='in_progress',
            debt=127000,
            conn_sales_order_id=sales_order
        )
        product = Product.objects.create(
            name="Teszt termék",
            net_price=10000,
            vat=27,
            free_stock=10,
            reserved_stock=0
        )
        invoice_item = InvoiceItem.objects.create(
            id=1,
            original_name='Teszt termék',
            original_producer='Teszt gyártó',
            original_net_price=100000,
            original_vat=18,
            original_package_quantity=8,
            original_package_display='karton',
            quantity=2,
            product_id=product,
            package_type_id=PackageType.objects.create(
                summary_name='teszt karton',
                display_name='karton',
                quantity=8
            ),
            invoice_id=invoice
        )

        self.assertEqual(str(invoice_item), f"#{invoice_item.invoice_id.id} - {invoice_item.original_name}")
        invoice.account_number_key = 1
        invoice.account_number = 'SZA-1'
        self.assertEqual(str(invoice_item), f"{invoice_item.invoice_id.account_number} - {invoice_item.original_name}")

        self.assertEqual(16000, invoice_item.get_original_net_price())
        self.assertEqual(18880, invoice_item.get_original_gross_price())