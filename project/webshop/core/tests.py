from django.test import TestCase
from django.test.client import Client
from django.shortcuts import reverse
from django.contrib.auth import get_user_model

from administration.sales_order.models import SalesOrder
from webshop.core.forms import AddressChangeForm, ContactForm
from webshop.core.models import FAQ, FAQTopic

User = get_user_model()

# FAQ tests

class FAQEmptyViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        User.objects.create_user(
            username='customer',
            email='customer@test.com',
            password='customer'
        )

    def test_get_faq_empty_list(self):
        # Bejelentkezés nélkül
        response = self.client.get(reverse('webshop_core:faq-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(u"Jelenleg egyetlen kérdés sem áll rendelkezésre." in response.content.decode('utf8'))

        # Vásárló fiókkal bejelentkezve
        self.client.login(username='customer', password='customer')
        response = self.client.get(reverse('webshop_core:faq-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(u"Jelenleg egyetlen kérdés sem áll rendelkezésre." in response.content.decode('utf8'))

class FAQViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        User.objects.create_user(
            username='customer',
            email='customer@test.com',
            password='customer'
        )
    
    @classmethod
    def setUpTestData(cls):
        topic = FAQTopic.objects.create(
            name='Teszt téma'
        )
        faq = FAQ.objects.create(
            question='Ez az első teszt kérdés',
            answer='Ez az első teszt válasz',
            topic_id=topic
        )
        faq2 = FAQ.objects.create(
            question='Ez a második teszt kérdés',
            answer='Ez a második teszt válasz',
            topic_id=topic
        )

    def test_get_faq_list(self):
        # Bejelentkezés nélkül
        response = self.client.get(reverse('webshop_core:faq-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(u"Gyakori kérdések" in response.content.decode('utf8'))
        self.assertTrue(u"Ez a második teszt válasz" in response.content.decode('utf8'))

        # Vásárló fiókkal bejelentkezve
        self.client.login(username='customer', password='customer')
        response = self.client.get(reverse('webshop_core:faq-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(u"Gyakori kérdések" in response.content.decode('utf8'))
        self.assertTrue(u"Teszt téma" in response.content.decode('utf8'))
        self.assertTrue(u"Ez az első teszt kérdés" in response.content.decode('utf8'))

# UserOrders tests

class UserOrdersEmptyViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        User.objects.create_user(
            username='customer',
            email='customer@test.com',
            password='customer'
        )

    def test_get_user_orders_empty_list(self):
        # Bejelentkezés nélkül
        response = self.client.get(reverse('webshop_core:user-orders'))
        self.assertEqual(response.status_code, 302)

        # Vásárló fiókkal bejelentkezve
        self.client.login(username='customer', password='customer')
        response = self.client.get(reverse('webshop_core:user-orders'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(u"Jelenleg nincs leadott rendelése." in response.content.decode('utf8'))

class UserOrdersViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(
            username='customer',
            email='customer@test.com',
            password='customer'
        )
        SalesOrder.objects.create(
            payment_type='cash',
            delivery_mode='delivery',
            net_price=100000,
            gross_price=127000,
            zip_code='2440',
            city='Százhalombatta',
            street_name='Valami utca',
            original_customer_name='Hegyi Dávid',
            customer_id=user,
            document_number_key=1,
            document_number='VME-1',
            status='in_progress'
        )

    def test_get_user_orders_list(self):
        # Bejelentkezés nélkül
        response = self.client.get(reverse('webshop_core:user-orders'))
        self.assertEqual(response.status_code, 302)

        # Vásárló fiókkal bejelentkezve
        self.client.login(username='customer', password='customer')
        response = self.client.get(reverse('webshop_core:user-orders'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(u"Rendelések" in response.content.decode('utf8'))
        self.assertTrue(u"VME-1" in response.content.decode('utf8'))
        self.assertTrue(u"1270 Ft" in response.content.decode('utf8'))

# UserData tests

class UserDataViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(
            username='customer',
            email='customer@test.com',
            password='customer'
        )

    def test_get_user_data_list(self):
        # Bejelentkezés nélkül
        response = self.client.get(reverse('webshop_core:user-data'))
        self.assertEqual(response.status_code, 302)

        # Vásárló fiókkal bejelentkezve
        self.client.login(username='customer', password='customer')
        response = self.client.get(reverse('webshop_core:user-data'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(u"Szállítási/Számlázási" in response.content.decode('utf8'))

class AddressChangeFormTest(TestCase):
    def test_address_change_form(self):
        # Kötelező mezők teszt
        empty_data = {
            'zip_code': '',
            'city': '',
            'street_name': '',
            'house_number': '',
        }
        form = AddressChangeForm(data=empty_data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)
        self.assertTrue('zip_code' in form.errors and 'city' in form.errors and 'street_name' in form.errors and 'house_number' in form.errors)

        # Hosszú adatok teszt
        long_data = {
            'zip_code': 'x'*11,
            'city': 'x'*101,
            'street_name': 'x'*101,
            'house_number': 'x'*21,
        }
        form = AddressChangeForm(data=long_data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)
        self.assertTrue('zip_code' in form.errors and 'city' in form.errors and 'street_name' in form.errors and 'house_number' in form.errors)

        # Helyes teszt
        valid_data = {
            'zip_code': '2440',
            'city': 'Százhalombatta',
            'street_name': 'Valami utca',
            'house_number': '11',
        }
        form = AddressChangeForm(data=valid_data)
        self.assertTrue(form.is_valid())

# Contact tests

class ContactViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(
            username='customer',
            email='customer@test.com',
            password='customer'
        )

    def test_get_user_orders_list(self):
        # Bejelentkezés nélkül
        response = self.client.get(reverse('webshop_core:contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(u"Elérhetőségek" in response.content.decode('utf8'))
        self.assertTrue(u"Székhely" in response.content.decode('utf8'))

        # Vásárló fiókkal bejelentkezve
        self.client.login(username='customer', password='customer')
        response = self.client.get(reverse('webshop_core:contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(u"Üzenetküldés" in response.content.decode('utf8'))
        self.assertTrue(u"Adószám" in response.content.decode('utf8'))
        self.assertTrue(u"Telefon" in response.content.decode('utf8'))

class ContactFormTest(TestCase):
    def test_contact_form(self):
        # Kötelező mezők teszt
        empty_data = {
            'first_name': '',
            'last_name': '',
            'email': '',
            'message': '',
        }
        form = ContactForm(data=empty_data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)
        self.assertTrue('first_name' in form.errors and 'last_name' in form.errors and 'email' in form.errors and 'message' in form.errors)

        # Hosszú adatok teszt
        long_data = {
            'first_name': 'x'*51,
            'last_name': 'x'*51,
            'email': 'test@test.com',
            'message': 'test',
        }
        form = ContactForm(data=long_data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)
        self.assertTrue('first_name' in form.errors and 'last_name' in form.errors)

        # Hibás e-mail teszt
        long_data = {
            'first_name': 'Teszt',
            'last_name': 'Jakab',
            'email': 'test.com',
            'message': 'test',
        }
        form = ContactForm(data=long_data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)
        self.assertTrue('email' in form.errors)

        # Helyes teszt
        valid_data = {
            'first_name': 'Teszt',
            'last_name': 'Jakab',
            'email': 'test@test.com',
            'message': 'test',
        }
        form = ContactForm(data=valid_data)
        self.assertTrue(form.is_valid())