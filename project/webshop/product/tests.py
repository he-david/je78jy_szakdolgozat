from django.test import TestCase
from django.test.client import Client
from django.shortcuts import reverse
from django.contrib.auth import get_user_model

from webshop.product.models import Category, Product

User = get_user_model()

# Product test

class ProductEmptyViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        User.objects.create_user(
            username='customer',
            email='customer@test.com',
            password='customer'
        )

    def test_get_product_empty_list(self):
        # Bejelentkezés nélkül
        response = self.client.get(reverse('webshop_product:product-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(u"Jelenleg egyetlen termék sem áll rendelkezésre." in response.content.decode('utf8'))

        # Vásárló fiókkal bejelentkezve
        self.client.login(username='customer', password='customer')
        response = self.client.get(reverse('webshop_product:product-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(u"Jelenleg egyetlen termék sem áll rendelkezésre." in response.content.decode('utf8'))

class ProductViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        User.objects.create_user(
            username='customer',
            email='customer@test.com',
            password='customer'
        )
    
    @classmethod
    def setUpTestData(cls):
        Product.objects.create(
            name="Teszt termék",
            producer='Teszt Gyártó',
            net_price=10000,
            vat=27,
            free_stock=100,
            reserved_stock=50,
            description='Ez itt a termék leírása.',
            category_id = Category.objects.create(
                name="Teszt kategória",
            )
        )

    def test_get_product_list(self):
        # Bejelentkezés nélkül
        response = self.client.get(reverse('webshop_product:product-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(u"Teszt termék" in response.content.decode('utf8'))
        self.assertTrue(u"127 Ft" in response.content.decode('utf8'))

        # Vásárló fiókkal bejelentkezve
        self.client.login(username='customer', password='customer')
        response = self.client.get(reverse('webshop_product:product-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(u"Teszt kategória" in response.content.decode('utf8'))

    def test_product_detail(self):
        # Bejelentkezés nélkül
        response = self.client.get(reverse('webshop_product:product-detail', kwargs={'slug': 'teszt-termek'}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(u"100" in response.content.decode('utf8'))
        self.assertTrue(u"Ez itt a termék leírása." in response.content.decode('utf8'))

        # Vásárló fiókkal bejelentkezve
        self.client.login(username='customer', password='customer')
        response = self.client.get(reverse('webshop_product:product-detail', kwargs={'slug': 'teszt-termek'}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(u"Teszt termék" in response.content.decode('utf8'))
        self.assertTrue(u"Teszt Gyártó" in response.content.decode('utf8'))

    def test_product_detail_404(self):
        response = self.client.get(reverse('webshop_product:product-detail', kwargs={'slug': 'nincs'}))
        self.assertEqual(response.status_code, 404)