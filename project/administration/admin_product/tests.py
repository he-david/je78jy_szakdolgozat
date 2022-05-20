from django.test import TestCase
from django.test.client import Client
from django.shortcuts import reverse
from django.contrib.auth import get_user_model

from datetime import timedelta, date
from administration.product_receipt.models import ProductReceipt, ProductReceiptItem

from webshop.product.models import Action, PackageType, Product
from webshop.cart.models import Cart, CartItem
from administration.admin_product.forms import ProductForm, ProductCreateForm, PackageForm
from administration.admin_product import utils as product_utils

User = get_user_model()

# Product

    # Views tests

class AdminProductViewTest(TestCase):
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
        Product.objects.create(
            id=1,
            name="Teszt termék",
            net_price=10000,
            vat=27,
            free_stock=100,
            reserved_stock=50
        )

    # ListView tests

    def test_get_product_list_with_superuser(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('admin_core:admin_product:product-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(u"Teszt termék" in response.content.decode('utf8'))
        self.assertTrue(u"100 Ft" in response.content.decode('utf8'))
        self.assertTrue(u"27%" in response.content.decode('utf8'))
        self.assertTrue(u"Új Termék" in response.content.decode('utf8'))

    def test_get_product_list_with_customer(self):
        # Bejelentkezés nélkül
        response = self.client.get(reverse('admin_core:admin_product:product-list'))
        self.assertEqual(response.status_code, 302)

        # Vásárló fiókkal bejelentkezve
        self.client.login(username='customer', password='customer')
        response = self.client.get(reverse('admin_core:admin_product:product-list'))
        self.assertEqual(response.status_code, 302)

    # DetailView tests

    def test_get_product_detail_with_superuser(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('admin_core:admin_product:product-detail', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Teszt termék módosítás")

    def test_get_product_detail_with_customer(self):
        # Bejelentkezés nélkül
        response = self.client.get(reverse('admin_core:admin_product:product-detail', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 302)

        # Vásárló fiókkal bejelentkezve
        self.client.login(username='customer', password='customer')
        response = self.client.get(reverse('admin_core:admin_product:product-detail', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 302)

    def test_get_product_detail_404(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('admin_core:admin_product:product-detail', kwargs={'id': 2}))
        self.assertEqual(response.status_code, 404)

    # CreateView tests

    def test_get_product_create_with_superuser(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('admin_core:admin_product:product-create'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Termék létrehozás")

    def test_get_product_create_with_customer(self):
        # Bejelentkezés nélkül
        response = self.client.get(reverse('admin_core:admin_product:product-create'))
        self.assertEqual(response.status_code, 302)

        # Vásárló fiókkal bejelentkezve
        self.client.login(username='customer', password='customer')
        response = self.client.get(reverse('admin_core:admin_product:product-create'))
        self.assertEqual(response.status_code, 302)

    # DeleteView tests

    def test_get_product_delete_with_superuser(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('admin_core:admin_product:product-delete', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Teszt termék nevű terméket")

    def test_get_product_delete_with_customer(self):
        # Bejelentkezés nélkül
        response = self.client.get(reverse('admin_core:admin_product:product-delete', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 302)

        # Vásárló fiókkal bejelentkezve
        self.client.login(username='customer', password='customer')
        response = self.client.get(reverse('admin_core:admin_product:product-delete', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 302)

    def test_get_product_delete_404(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('admin_core:admin_product:product-delete', kwargs={'id': 3}))
        self.assertEqual(response.status_code, 404)
    
    # Form tests

class ProductFormTest(TestCase):
    def test_product_form(self):
        # Kötelező mezők teszt
        empty_data = {
            'name': '',
            'producer': '',
            'net_price': '',
            'vat': '',
            'description': '',
            'free_stock': '',
            'reserved_stock': '',
            'image': '',
            'category_id': '',
            'package_type_id': '',
            'action_id': ''
        }
        form = ProductForm(data=empty_data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)
        self.assertTrue('name' in form.errors and 'producer' in form.errors and 'net_price' in form.errors and 'vat' in form.errors and 'free_stock' in form.errors and 'reserved_stock' in form.errors and 'package_type_id' in form.errors)

        # Hosszú név teszt
        long_name_data = {
            'name': 'x'*101,
            'producer': 'teszt',
            'net_price': 10000,
            'vat': 27,
            'description': 'teszt',
            'free_stock': 100,
            'reserved_stock': 50,
            'image': '',
            'category_id': None,
            'package_type_id': '',
            'action_id': ''
        }
        form = ProductForm(data=long_name_data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)
        self.assertTrue('name' in form.errors and 'producer' not in form.errors)

        # Hosszú név teszt
        long_producer_data = {
            'name': 'teszt',
            'producer': 'x'*101,
            'net_price': 10000,
            'vat': 27,
            'description': 'teszt',
            'free_stock': 100,
            'reserved_stock': 50,
            'image': '',
            'category_id': None,
            'package_type_id': '',
            'action_id': ''
        }
        form = ProductCreateForm(data=long_producer_data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)
        self.assertTrue('producer' in form.errors and 'name' not in form.errors)

    def test_product_create_form(self):
        # Kötelező mezők teszt
        empty_data = {
            'name': '',
            'producer': '',
            'net_price': '',
            'vat': '',
            'description': '',
            'image': '',
            'category_id': '',
            'package_type_id': '',
            'action_id': ''
        }
        form = ProductCreateForm(data=empty_data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)
        self.assertTrue('name' in form.errors and 'producer' in form.errors and 'net_price' in form.errors and 'vat' in form.errors and 'package_type_id' in form.errors)

        # Hosszú név teszt
        long_name_data = {
            'name': 'x'*101,
            'producer': 'teszt',
            'net_price': 10000,
            'vat': 27,
            'description': 'teszt',
            'image': '',
            'category_id': None,
            'package_type_id': '',
            'action_id': ''
        }
        form = ProductCreateForm(data=long_name_data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)
        self.assertTrue('name' in form.errors and 'producer' not in form.errors)

        # Hosszú név teszt
        long_producer_data = {
            'name': 'teszt',
            'producer': 'x'*101,
            'net_price': 10000,
            'vat': 27,
            'description': 'teszt',
            'image': '',
            'category_id': None,
            'package_type_id': '',
            'action_id': ''
        }
        form = ProductCreateForm(data=long_producer_data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)
        self.assertTrue('producer' in form.errors and 'name' not in form.errors)

    # Model tests

class ProductModelTest(TestCase):
    def test_product_model(self):
        product = Product.objects.create(
            id=1,
            name="Teszt termék",
            net_price=10000,
            vat=27,
            free_stock=100,
            reserved_stock=50
        )
        self.assertEqual(str(product), product.name)
        self.assertIn('teszt-termek', product.get_absolute_url())
        self.assertNotIn(str(product.id), product.get_absolute_url())

        self.assertIn(str(product.id), product.get_absolute_admin_url())
        self.assertNotIn('teszt-termek', product.get_absolute_admin_url())

    def test_product_action(self):
        product = Product.objects.create(
            id=1,
            name="Teszt termék",
            net_price=10000,
            vat=27,
            free_stock=100,
            reserved_stock=50
        )
        self.assertEqual(0, product.get_action_percent())

        old_action = Action.objects.create(
            name="Régi akció",
            percent=60,
            from_date=date.today() - timedelta(days=5),
            to_date=date.today() - timedelta(days=1)
        )
        product.action_id.add(old_action)
        self.assertEqual(0, product.get_action_percent())


        curr_action = Action.objects.create(
            name="Aktuális akció",
            percent=30,
            from_date=date.today(),
            to_date=date.today() + timedelta(days=7)
        )
        product.action_id.add(curr_action)
        self.assertEqual(30, product.get_action_percent())

        curr_better_action = Action.objects.create(
            name="Jobb akció",
            percent=50,
            from_date=date.today() - timedelta(days=2),
            to_date=date.today() + timedelta(days=7)
        )
        product.action_id.add(curr_better_action)
        self.assertEqual(50, product.get_action_percent())

    def test_product_stock(self):
        product = Product.objects.create(
            id=1,
            name="Teszt termék",
            net_price=10000,
            vat=27,
            free_stock=100,
            reserved_stock=50
        )
        self.assertEqual(0, product.get_positive_stock_movement_sum())
        self.assertTrue(product.has_no_open_document())

        pr = ProductReceipt.objects.create(
            status = 'final',
        )
        ProductReceiptItem.objects.create(
            original_name = "Teszt",
            quantity = 10,
            product_id = product,
            product_receipt_id= pr
        )
        ProductReceiptItem.objects.create(
            original_name = "Teszt2",
            quantity = 5,
            product_id = product,
            product_receipt_id= pr
        )
        self.assertEqual(15, product.get_positive_stock_movement_sum())
        self.assertEqual(0, product.get_negative_stock_movement_sum())
        self.assertTrue(product.has_no_open_document())

        ProductReceiptItem.objects.create(
            original_name = "Teszt3",
            quantity = 5,
            product_id = product,
            product_receipt_id= ProductReceipt.objects.create(status='in_progress')
        )

    # Utils tests

class ProductUtilsTest(TestCase):
    def test_product_stock_movement(self):
        product = Product.objects.create(
            id=1,
            name="Teszt termék",
            net_price=10000,
            vat=27,
            free_stock=0,
            reserved_stock=0
        )
        self.assertEqual(0, product.free_stock)
        self.assertEqual(0, product.reserved_stock)
        product_utils.recover_stock_to_free(product, 10)
        self.assertEqual(10, product.free_stock)
        product_utils.reserve_stock(product, 6)
        self.assertEqual(4, product.free_stock)
        self.assertEqual(6, product.reserved_stock)
        product_utils.free_stock(product, 4)
        self.assertEqual(8, product.free_stock)
        self.assertEqual(2, product.reserved_stock)
        product_utils.remove_stock(product, 1)
        self.assertEqual(1, product.reserved_stock)
        product_utils.recover_stock_to_reserved(product, 9)
        self.assertEqual(10, product.reserved_stock)

    def test_cart_items(self):
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
        self.assertTrue(len(product_utils.get_product_with_less_stock(cart)) == 0)
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
        self.assertTrue(len(product_utils.get_product_with_less_stock(cart)) == 1)

# PackageType

    # Views tests

class PackageTypeViewTest(TestCase):
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
        PackageType.objects.create(
            summary_name='darab',
            display_name='db',
            quantity=1
        )

    # ListView tests

    def test_get_package_list_with_superuser(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('admin_core:admin_product:package-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(u"darab" in response.content.decode('utf8'))
        self.assertTrue(u"Új Kiszerelés" in response.content.decode('utf8'))

    def test_get_package_list_without_superuser(self):
        # Bejelentkezés nélkül
        response = self.client.get(reverse('admin_core:admin_product:package-list'))
        self.assertEqual(response.status_code, 302)

        # Vásárló fiókkal bejelentkezve
        self.client.login(username='customer', password='customer')
        response = self.client.get(reverse('admin_core:admin_product:package-list'))
        self.assertEqual(response.status_code, 302)

    # DetailView tests

    def test_get_package_detail_with_superuser(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('admin_core:admin_product:package-detail', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "darab módosítás")

    def test_get_package_detail_with_customer(self):
        # Bejelentkezés nélkül
        response = self.client.get(reverse('admin_core:admin_product:package-detail', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 302)

        # Vásárló fiókkal bejelentkezve
        self.client.login(username='customer', password='customer')
        response = self.client.get(reverse('admin_core:admin_product:package-detail', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 302)

    def test_get_package_detail_404(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('admin_core:admin_product:package-detail', kwargs={'id': 5}))
        self.assertEqual(response.status_code, 404)

    # CreateView tests

    def test_get_package_create_with_superuser(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('admin_core:admin_product:package-create'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Kiszerelés létrehozás")

    def test_get_package_create_with_customer(self):
        # Bejelentkezés nélkül
        response = self.client.get(reverse('admin_core:admin_product:package-create'))
        self.assertEqual(response.status_code, 302)

        # Vásárló fiókkal bejelentkezve
        self.client.login(username='customer', password='customer')
        response = self.client.get(reverse('admin_core:admin_product:package-create'))
        self.assertEqual(response.status_code, 302)

    # DeleteView tests

    def test_get_package_delete_with_superuser(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('admin_core:admin_product:package-delete', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "darab nevű kiszerelést")

    def test_get_package_delete_with_customer(self):
        # Bejelentkezés nélkül
        response = self.client.get(reverse('admin_core:admin_product:package-delete', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 302)

        # Vásárló fiókkal bejelentkezve
        self.client.login(username='customer', password='customer')
        response = self.client.get(reverse('admin_core:admin_product:package-delete', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 302)

    def test_get_package_delete_404(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('admin_core:admin_product:package-delete', kwargs={'id': 5}))
        self.assertEqual(response.status_code, 404)

    # Form tests

class PackageFormTest(TestCase):
    def test_package_form(self):
        # Kötelező mezők teszt
        empty_data = {
            'summary_name': '',
            'display_name': '',
            'quantity': '',
        }
        form = PackageForm(data=empty_data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)
        self.assertTrue('summary_name' in form.errors and 'display_name' in form.errors and 'quantity' in form.errors)

        # Hosszú nevek teszt
        long_name_data = {
            'summary_name': 'x'*51,
            'display_name': 'x'*51,
            'quantity': 1
        }
        form = PackageForm(data=long_name_data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)
        self.assertTrue('summary_name' in form.errors and 'display_name' in form.errors)

        # Helyes teszt
        valid_data = {
            'summary_name': 'darab',
            'display_name': 'db',
            'quantity': 1
        }
        form = PackageForm(data=valid_data)
        self.assertTrue(form.is_valid())

    # Model tests

class PackageModelTest(TestCase):
    def test_package_model(self):
        package = PackageType.objects.create(
            id=3,
            summary_name='darab',
            display_name='db',
            quantity=1
        )

        self.assertEqual(str(package), package.summary_name)
        self.assertIn(str(package.id), package.get_absolute_admin_url())
        self.assertNotIn('1', package.get_absolute_admin_url())

        self.assertTrue(package.is_deletable())

        product = Product.objects.create(
            name="Teszt termék",
            net_price=10000,
            vat=27,
            free_stock=0,
            reserved_stock=0
        )
        product.package_type_id.add(package)
        self.assertFalse(package.is_deletable())
