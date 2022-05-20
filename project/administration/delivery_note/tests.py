from django.test import TestCase
from django.test.client import Client
from django.shortcuts import reverse
from django.contrib.auth import get_user_model

from administration.delivery_note.models import DeliveryNote, DeliveryNoteItem
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
        delivery_note = DeliveryNote.objects.create(
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
            document_number='SZL-1',
            status='in_progress',
            conn_sales_order_id=sales_order
        )
        DeliveryNoteItem.objects.create(
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
            delivery_note_id=delivery_note
        )

    # ListView tests

    def test_get_delivery_note_list_with_superuser(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('admin_core:admin_delivery_note:delivery-note-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(u"SZL-1" in response.content.decode('utf8'))
        self.assertTrue(u"Folyamatban" in response.content.decode('utf8'))

    def test_get_delivery_note_list_without_superuser(self):
        # Bejelentkezés nélkül
        response = self.client.get(reverse('admin_core:admin_delivery_note:delivery-note-list'))
        self.assertEqual(response.status_code, 302)

        # Vásárló fiókkal bejelentkezve
        self.client.login(username='customer', password='customer')
        response = self.client.get(reverse('admin_core:admin_delivery_note:delivery-note-list'))
        self.assertEqual(response.status_code, 302)

    # DetailView tests

    def test_get_delivery_note_detail_with_superuser(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('admin_core:admin_delivery_note:delivery-note-detail', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Szállítólevél módosítás")
        self.assertContains(response, "Teljesítés")
        self.assertContains(response, "Törlés")

    def test_get_delivery_note_detail_with_customer(self):
        # Bejelentkezés nélkül
        response = self.client.get(reverse('admin_core:admin_delivery_note:delivery-note-detail', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 302)

        # Vásárló fiókkal bejelentkezve
        self.client.login(username='customer', password='customer')
        response = self.client.get(reverse('admin_core:admin_delivery_note:delivery-note-detail', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 302)

    def test_get_delivery_note_detail_404(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('admin_core:admin_delivery_note:delivery-note-detail', kwargs={'id': 5}))
        self.assertEqual(response.status_code, 404)

# Model tests

class DeliveryNoteModelTest(TestCase):
    def test_delivery_note_model(self):
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
        delivery_note = DeliveryNote.objects.create(
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
            conn_sales_order_id=sales_order
        )
        self.assertEqual(str(delivery_note), f"#{delivery_note.id}")
        delivery_note.document_number_key=1
        delivery_note.document_number='SZL-1'
        self.assertEqual(str(delivery_note), delivery_note.document_number)

        self.assertIn(str(delivery_note.id), delivery_note.get_absolute_url())
        self.assertNotIn('2', delivery_note.get_absolute_url())

        self.assertEqual(1000, delivery_note.get_net_price())
        self.assertEqual(1270, delivery_note.get_gross_price())

    def test_delivery_note_item_model(self):
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
        delivery_note = DeliveryNote.objects.create(
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
            conn_sales_order_id=sales_order
        )
        product = Product.objects.create(
            name="Teszt termék",
            net_price=10000,
            vat=27,
            free_stock=10,
            reserved_stock=0
        )
        delivery_note_item = DeliveryNoteItem.objects.create(
            id=1,
            original_name='Teszt termék',
            original_producer='Teszt gyártó',
            original_net_price=100000,
            original_vat=27,
            original_package_quantity=5,
            original_package_display='db',
            quantity=1,
            product_id=product,
            package_type_id=PackageType.objects.create(
                summary_name='darab',
                display_name='db',
                quantity=1
            ),
            delivery_note_id=delivery_note
        )

        self.assertEqual(str(delivery_note_item), f"#{delivery_note_item.delivery_note_id.id} - {delivery_note_item.original_name}")
        delivery_note.document_number_key = 1
        delivery_note.document_number = 'SZL-1'
        self.assertEqual(str(delivery_note_item), f"{delivery_note_item.delivery_note_id.document_number} - {delivery_note_item.original_name}")

        self.assertEqual(5000, delivery_note_item.get_original_net_price())
        self.assertEqual(6350, delivery_note_item.get_original_gross_price())