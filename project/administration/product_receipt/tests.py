from django.test import TestCase
from django.test.client import Client
from django.contrib.auth import get_user_model
from django.shortcuts import reverse

from datetime import date

from administration.product_receipt.forms import ProductReceiptForm, ProductReceiptItemForm
from administration.product_receipt.models import ProductReceipt, ProductReceiptItem
from webshop.product.models import Product
from administration.product_receipt import utils

User = get_user_model()

# ProductReceipt

    # Views tests

class ProductReceiptViewTest(TestCase):
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
        pr = ProductReceipt.objects.create(
            id=42,
            document_number_key=1,
            document_number='BEV-1',
            status='in_progress',
            sum_quantity=10
        )
        product = Product.objects.create(
            id=1,
            name="Teszt termék",
            net_price=10000,
            vat=27,
            free_stock=100,
            reserved_stock=50
        )
        ProductReceiptItem.objects.create(
            original_name='Teszt termék',
            quantity=10,
            product_id=product,
            product_receipt_id=pr
        )

    # ListView tests

    def test_get_product_receipt_list_with_superuser(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('admin_core:admin_product_receipt:product-receipt-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(u"BEV-1" in response.content.decode('utf8'))
        self.assertTrue(u"Új Bevételezés" in response.content.decode('utf8'))

    def test_get_product_receipt_list_without_superuser(self):
        # Bejelentkezés nélkül
        response = self.client.get(reverse('admin_core:admin_product_receipt:product-receipt-list'))
        self.assertEqual(response.status_code, 302)

        # Vásárló fiókkal bejelentkezve
        self.client.login(username='customer', password='customer')
        response = self.client.get(reverse('admin_core:admin_product_receipt:product-receipt-list'))
        self.assertEqual(response.status_code, 302)

    # DetailView tests

    def test_get_product_receipt_detail_with_superuser(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('admin_core:admin_product_receipt:product-receipt-detail', kwargs={'id': 42}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Teszt termék")
        self.assertContains(response, "Bevételezés módosítás")

    def test_get_product_receipt_detail_with_customer(self):
        # Bejelentkezés nélkül
        response = self.client.get(reverse('admin_core:admin_product_receipt:product-receipt-detail', kwargs={'id': 42}))
        self.assertEqual(response.status_code, 302)

        # Vásárló fiókkal bejelentkezve
        self.client.login(username='customer', password='customer')
        response = self.client.get(reverse('admin_core:admin_product_receipt:product-receipt-detail', kwargs={'id': 42}))
        self.assertEqual(response.status_code, 302)

    def test_get_product_receipt_detail_404(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('admin_core:admin_product_receipt:product-receipt-detail', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 404)

    # DeleteView tests

    def test_get_product_receipt_delete_with_superuser(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('admin_core:admin_product_receipt:product-receipt-delete', kwargs={'id': 42}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "BEV-1 bizonylatszámú bevételezést")

    def test_get_product_receipt_delete_with_customer(self):
        # Bejelentkezés nélkül
        response = self.client.get(reverse('admin_core:admin_product_receipt:product-receipt-delete', kwargs={'id': 42}))
        self.assertEqual(response.status_code, 302)

        # Vásárló fiókkal bejelentkezve
        self.client.login(username='customer', password='customer')
        response = self.client.get(reverse('admin_core:admin_product_receipt:product-receipt-delete', kwargs={'id': 42}))
        self.assertEqual(response.status_code, 302)

    def test_get_product_receipt_delete_404(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('admin_core:admin_product_receipt:product-receipt-delete', kwargs={'id': 2}))
        self.assertEqual(response.status_code, 404)

    # Form tests

class ProductReceiptFormTest(TestCase):
    def test_product_receipt_form(self):
        # Kötelező mezők teszt
        empty_data = {
            'status': '',
            'finalization_date': '',
            'document_number': '',
            'sum_quantity': '',
        }
        form = ProductReceiptForm(data=empty_data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)
        self.assertTrue('sum_quantity' in form.errors)

        # Hosszú bizonylatszám teszt
        long_data = {
            'status': 'in_progress',
            'finalization_date': date.today(),
            'document_number': 'x'*21,
            'sum_quantity': 10,
        }
        form = ProductReceiptForm(data=long_data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)
        self.assertTrue('document_number' in form.errors)

        # Helyes teszt
        valid_data = {
            'status': 'in_progress',
            'finalization_date': date.today(),
            'document_number': 'BEV-1',
            'sum_quantity': 10,
        }
        form = ProductReceiptForm(data=valid_data)
        self.assertTrue(form.is_valid())

    # Model tests

class ProductReceiptModelTest(TestCase):
    def test_product_receipt_model(self):
        pr = ProductReceipt.objects.create(
            id=42,
            document_number_key=1,
            document_number='BEV-1',
            status='in_progress',
            sum_quantity=10
        )
        self.assertEquals(pr.document_number, str(pr))
        self.assertIn(str(pr.id), pr.get_absolute_url())
        self.assertNotIn('1', pr.get_absolute_url())

    # Utils tests

class ProductReceiptUtilsTest(TestCase):
    def test_product_receipt_create(self):
        product = Product.objects.create(
            name="Teszt termék",
            net_price=10000,
            vat=27,
            free_stock=100,
            reserved_stock=50
        )
        pr = utils.create_product_receipt()

        self.assertTrue(pr.status == 'in_progress' and pr.document_number is None)
        item = ProductReceiptItem.objects.create(
            original_name='Teszt termék',
            quantity=10,
            product_id=product,
            product_receipt_id=pr
        )
        utils.create_product_receipt_item(item, pr.id)
        self.assertEqual(pr, item.product_receipt_id)

        utils.change_product_receipt_sum_quantity(pr, 20)
        self.assertEqual(20, pr.sum_quantity)

        utils.finalize_product_receipt(pr)
        self.assertEqual('BEV-1', pr.document_number)
        self.assertEqual('final', pr.status)

# ProductReceiptItem

    # Views tests

class ProductReceiptItemViewTest(TestCase):
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
        pr = ProductReceipt.objects.create(
            id=42,
            document_number_key=1,
            document_number='BEV-1',
            status='in_progress',
            sum_quantity=10
        )
        product = Product.objects.create(
            id=1,
            name="Teszt termék",
            net_price=10000,
            vat=27,
            free_stock=100,
            reserved_stock=50
        )
        ProductReceiptItem.objects.create(
            id=5,
            original_name='Teszt termék',
            quantity=10,
            product_id=product,
            product_receipt_id=pr
        )
        ProductReceiptItem.objects.create(
            id=6,
            original_name='Teszt termék',
            quantity=5,
            product_id=product,
            product_receipt_id=pr
        )

    # CreateView tests

    def test_get_product_receipt_item_create_with_superuser(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('admin_core:admin_product_receipt:product-receipt-item-create', kwargs={'id': 42}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Bevételezés tétel létrehozás")

    def test_get_product_receipt_item_create_with_customer(self):
        # Bejelentkezés nélkül
        response = self.client.get(reverse('admin_core:admin_product_receipt:product-receipt-item-create', kwargs={'id': 42}))
        self.assertEqual(response.status_code, 302)

        # Vásárló fiókkal bejelentkezve
        self.client.login(username='customer', password='customer')
        response = self.client.get(reverse('admin_core:admin_product_receipt:product-receipt-item-create', kwargs={'id': 42}))
        self.assertEqual(response.status_code, 302)

    # DeleteView tests

    def test_get_product_receipt_item_delete_with_superuser(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('admin_core:admin_product_receipt:product-receipt-item-delete', kwargs={'id': 5}))
        self.assertEqual(response.status_code, 302)

    def test_get_product_receipt_item_delete_with_customer(self):
        # Bejelentkezés nélkül
        response = self.client.get(reverse('admin_core:admin_product_receipt:product-receipt-item-delete', kwargs={'id': 6}))
        self.assertEqual(response.status_code, 302)

        # Vásárló fiókkal bejelentkezve
        self.client.login(username='customer', password='customer')
        response = self.client.get(reverse('admin_core:admin_product_receipt:product-receipt-item-delete', kwargs={'id': 6}))
        self.assertEqual(response.status_code, 302)

    # Form tests

class ProductReceiptItemFormTest(TestCase):
    
    def test_product_receipt_item_form(self):
        # Kötelező mezők teszt
        empty_data = {
            'quantity': '',
            'product_id': '',
        }
        form = ProductReceiptItemForm(data=empty_data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)
        self.assertTrue('quantity' in form.errors and 'product_id' in form.errors)

        # Helyes teszt
        product = Product.objects.create(
            name="Teszt termék",
            net_price=10000,
            vat=27,
            free_stock=100,
            reserved_stock=50
        )
        valid_data = {
            'quantity': 10,
            'product_id': product
        }
        form = ProductReceiptItemForm(data=valid_data)
        self.assertTrue(form.is_valid())