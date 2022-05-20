from django.test import TestCase
from django.test.client import Client
from django.shortcuts import reverse
from django.contrib.auth import get_user_model

from administration.delivery_note.models import DeliveryNote
from webshop.cart.forms import PaymentOrderDataForm
from webshop.cart.models import Cart, CartItem
from administration.sales_order.models import SalesOrderItem, SalesOrder
from administration.invoice.models import Invoice
from webshop.product.models import PackageType, Product
from administration.sales_order import utils as sales_order_utils
from administration.invoice import utils as invoice_utils
from administration.delivery_note import utils as delivery_note_utils
from webshop.core.models import Address

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
        SalesOrderItem.objects.create(
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
            sales_order_id=sales_order
        )

    # ListView tests

    def test_get_sales_order_list_with_superuser(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('admin_core:admin_sales_order:sales-order-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(u"VME-1" in response.content.decode('utf8'))
        self.assertTrue(u"Folyamatban" in response.content.decode('utf8'))

    def test_get_sales_order_list_without_superuser(self):
        # Bejelentkezés nélkül
        response = self.client.get(reverse('admin_core:admin_sales_order:sales-order-list'))
        self.assertEqual(response.status_code, 302)

        # Vásárló fiókkal bejelentkezve
        self.client.login(username='customer', password='customer')
        response = self.client.get(reverse('admin_core:admin_sales_order:sales-order-list'))
        self.assertEqual(response.status_code, 302)

    # DetailView tests

    def test_get_sales_order_detail_with_superuser(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('admin_core:admin_sales_order:sales-order-detail', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Megrendelés módosítás")
        self.assertContains(response, "Számla generálás")

    def test_get_sales_order_detail_with_customer(self):
        # Bejelentkezés nélkül
        response = self.client.get(reverse('admin_core:admin_sales_order:sales-order-detail', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 302)

        # Vásárló fiókkal bejelentkezve
        self.client.login(username='customer', password='customer')
        response = self.client.get(reverse('admin_core:admin_sales_order:sales-order-detail', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 302)

    def test_get_sales_order_detail_404(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('admin_core:admin_sales_order:sales-order-detail', kwargs={'id': 5}))
        self.assertEqual(response.status_code, 404)

# Model tests

class SalesOrderModelTest(TestCase):
    def test_sales_order_model(self):
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
        self.assertEqual(str(sales_order), f"#{sales_order.id}")
        sales_order.document_number_key = 1
        sales_order.document_number = 'VME-1'
        self.assertEqual(str(sales_order), sales_order.document_number)

        self.assertIn(str(sales_order.id), sales_order.get_absolute_url())
        self.assertNotIn('2', sales_order.get_absolute_url())

        self.assertEqual(1000, sales_order.get_net_price())
        self.assertEqual(1270, sales_order.get_gross_price())

        self.assertFalse(sales_order.has_invoice())
        self.assertFalse(sales_order.has_view_invoice())
        self.assertFalse(sales_order.has_delivery_note())
        self.assertFalse(sales_order.has_view_delivery_note())

    def test_sales_order_item_model(self):
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
        product = Product.objects.create(
            id=1,
            name="Teszt termék",
            net_price=10000,
            vat=27,
            free_stock=10,
            reserved_stock=0
        )
        sales_order_item = SalesOrderItem.objects.create(
            original_name='Teszt termék',
            original_producer='Teszt gyártó',
            original_net_price=100000,
            original_vat=27,
            original_package_quantity=6,
            original_package_display='karton',
            quantity=3,
            product_id=product,
            package_type_id=PackageType.objects.create(
                summary_name='teszt karton',
                display_name='karton',
                quantity=6
            ),
            sales_order_id=sales_order
        )

        self.assertEqual(str(sales_order_item), f"#{sales_order_item.sales_order_id.id} - {sales_order_item.original_name}")
        sales_order.document_number_key = 1
        sales_order.document_number = 'VME-1'
        self.assertEqual(str(sales_order_item), f"{sales_order_item.sales_order_id.document_number} - {sales_order_item.original_name}")

        self.assertEqual(18000, sales_order_item.get_original_net_price())
        self.assertEqual(22860, sales_order_item.get_original_gross_price())

# Utils tests

class SalesOrderUtilsTest(TestCase):
    def test_sales_order(self):
        form_data = {
            'payment_type': 'cash',
            'delivery_mode': 'delivery'
        }
        form = PaymentOrderDataForm(data=form_data)
        form.is_valid()
        product = Product.objects.create(
            id=1,
            name="Teszt termék",
            net_price=10000,
            vat=27,
            free_stock=10,
            reserved_stock=0
        )
        cart_owner = User.objects.create_user(
            username='customer',
            email='customer@test.com',
            password='customer'
        )
        cart = Cart.objects.create(customer_id=cart_owner)
        CartItem.objects.create(
            quantity=5,
            product_id=product,
            cart_id=cart,
            package_type_id=PackageType.objects.create(
                summary_name='darab',
                display_name='db',
                quantity=1
            )
        )
        CartItem.objects.create(
            quantity=1,
            product_id=product,
            cart_id=cart,
            package_type_id=PackageType.objects.create(
                summary_name='karton',
                display_name='karton',
                quantity=6
            )
        )
        Address.objects.create(
            zip_code='2440',
            city='Százhalombatta',
            street_name='Valami utca',
            house_number='11',
            customer_id=cart_owner
        )
        sales_order_utils.create_sales_order(form, cart)
        sales_order = SalesOrder.objects.get(id=1)

        self.assertEqual(sales_order.document_number, 'VME-1')
        self.assertEqual(2, len(sales_order.items.all()))

        sales_order.status = 'partially_completed'
        sales_order_utils.cancel_sales_order(sales_order)
        self.assertEqual(sales_order.status, 'cancelled')

        # SalesOrder, Invoice, DeliveryNote status test

        sales_order.deleted = False
        sales_order.status = 'partially_completed'
        sales_order_utils.set_sales_order_status(sales_order)
        self.assertEqual(sales_order.status, 'in_progress')

        invoice_utils.create_invoice(sales_order)
        invoice = Invoice.objects.filter(conn_sales_order_id=sales_order, deleted=False).first()
        self.assertEqual(sales_order.status, 'partially_completed')
        self.assertEqual(invoice.status, 'in_progress')
        invoice_utils.invoice_settlement(invoice, sales_order)
        self.assertEqual(invoice.status, 'completed')
        invoice_utils.cancel_invoice(invoice, True)
        self.assertEqual(invoice.status, 'cancelled')

        delivery_note_utils.create_delivery_note(sales_order)
        delivery_note = DeliveryNote.objects.filter(conn_sales_order_id=sales_order, deleted=False).first()
        self.assertEqual(sales_order.status, 'partially_completed')
        invoice_utils.create_invoice(sales_order)
        invoice = Invoice.objects.filter(conn_sales_order_id=sales_order, deleted=False).first()
        delivery_note_utils.delete_delivery_note(delivery_note)
        invoice_utils.delete_invoice(invoice)

        delivery_note_utils.create_delivery_note(sales_order)
        delivery_note = DeliveryNote.objects.filter(conn_sales_order_id=sales_order, deleted=False).first()
        self.assertEqual(delivery_note.status, 'in_progress')
        invoice_utils.create_invoice(sales_order)
        invoice = Invoice.objects.filter(conn_sales_order_id=sales_order, deleted=False).first()
        self.assertEqual(invoice.status, 'in_progress')
        delivery_note_utils.delivery_note_completion(delivery_note, sales_order)
        self.assertEqual(delivery_note.status, 'completed')
        delivery_note_utils.cancel_delivery_note(delivery_note)
        self.assertEqual(delivery_note.status, 'cancelled')

        delivery_note_utils.create_delivery_note(sales_order)
        delivery_note = DeliveryNote.objects.filter(conn_sales_order_id=sales_order, deleted=False).first()
        self.assertEqual(delivery_note.status, 'in_progress')
        delivery_note_utils.delivery_note_completion(delivery_note, sales_order)
        invoice_utils.invoice_settlement(invoice, sales_order)
        self.assertEqual(invoice.status, 'completed')
        self.assertEqual(delivery_note.status, 'completed')
        self.assertEqual(sales_order.status, 'completed')
