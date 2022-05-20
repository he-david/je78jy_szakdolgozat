from django.test import TestCase
from django.test.client import Client
from django.shortcuts import reverse
from django.contrib.auth import get_user_model

from webshop.cart.models import Cart, CartItem
from webshop.product.models import PackageType, Product
from webshop.cart.forms import PaymentOrderDataForm, PaymentPersonalForm

User = get_user_model()

# Cart tests

class CartEmptyViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        User.objects.create_user(
            username='customer',
            email='customer@test.com',
            password='customer'
        )

    def test_get_cart_empty_list(self):
        # Bejelentkezés nélkül
        response = self.client.get(reverse('webshop_cart:summary'))
        self.assertEqual(response.status_code, 302)

        # Vásárló fiókkal bejelentkezve
        self.client.login(username='customer', password='customer')
        response = self.client.get(reverse('webshop_cart:summary'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(u"Jelenleg egy termék sincs a kosárban." in response.content.decode('utf8'))

class CartViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        
    
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(
            username='customer',
            email='customer@test.com',
            password='customer'
        )
        product = Product.objects.create(
            name="Teszt termék",
            net_price=10000,
            vat=27,
            free_stock=10,
            reserved_stock=0
        )
        cart = Cart.objects.create(customer_id=user)
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

    def test_get_cart_list(self):
        # Bejelentkezés nélkül
        response = self.client.get(reverse('webshop_cart:summary'))
        self.assertEqual(response.status_code, 302)

        # Vásárló fiókkal bejelentkezve
        self.client.login(username='customer', password='customer')
        response = self.client.get(reverse('webshop_cart:summary'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(u"Rendelés véglegesítése" in response.content.decode('utf8'))
        self.assertTrue(u"Teszt termék" in response.content.decode('utf8'))
        self.assertTrue(u"db" in response.content.decode('utf8'))

# PaymentPersonal test

class PaymentPersonalFormTest(TestCase):
    def test_payment_personal_form(self):
        # Kötelező mezők teszt
        empty_data = {
            'first_name': '',
            'last_name': '',
        }
        form = PaymentPersonalForm(data=empty_data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)
        self.assertTrue('first_name' in form.errors and 'last_name' in form.errors)

        # Hosszú adatok teszt
        long_data = {
            'first_name': 'x'*51,
            'last_name': 'x'*51,
        }
        form = PaymentPersonalForm(data=long_data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)
        self.assertTrue('first_name' in form.errors and 'last_name' in form.errors)

        # Helyes teszt
        valid_data = {
            'first_name': 'Teszt',
            'last_name': 'Jakab',
        }
        form = PaymentPersonalForm(data=valid_data)
        self.assertTrue(form.is_valid())

# PaymentOrderData test

class PaymentOrderDataFormTest(TestCase):
    def test_payment_order_data_form(self):
        # Kötelező mezők teszt
        empty_data = {
            'payment_type': '',
            'delivery_mode': '',
        }
        form = PaymentOrderDataForm(data=empty_data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)
        self.assertTrue('payment_type' in form.errors and 'delivery_mode' in form.errors)

        # Helytelen választás teszt
        invalid_choice_data = {
            'payment_type': 'ilyen fizetés nincs',
            'delivery_mode': 'ilyen szállítás nincs',
        }
        form = PaymentOrderDataForm(data=invalid_choice_data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)
        self.assertTrue('payment_type' in form.errors and 'delivery_mode' in form.errors)

        # Helyes teszt
        valid_data = {
            'first_name': 'cash',
            'last_name': 'delivery',
        }
        form = PaymentPersonalForm(data=valid_data)
        self.assertTrue(form.is_valid())

# PaymentSuccess test

class PaymentSuccessViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        User.objects.create_user(
            username='customer',
            email='customer@test.com',
            password='customer'
        )

    def test_payment_success_view(self):
        # Bejelentkezés nélkül
        response = self.client.get(reverse('webshop_cart:payment-success'))
        self.assertEqual(response.status_code, 302)

        # Vásárló fiókkal bejelentkezve
        self.client.login(username='customer', password='customer')
        response = self.client.get(reverse('webshop_cart:payment-success'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(u"Köszönjük a rendelését!" in response.content.decode('utf8'))