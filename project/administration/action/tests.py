from django.test import TestCase
from django.test.client import Client
from django.shortcuts import reverse
from django.contrib.auth import get_user_model

from datetime import date, timedelta

from webshop.product.models import Action
from administration.action.forms import ActionForm

User = get_user_model()

# Views tests

class ActionViewTest(TestCase):
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
        Action.objects.create(
            id=1,
            name="Teszt akció",
            percent=30,
            from_date=date.today(),
            to_date=date.today() + timedelta(days=7)
        )

    # ListView tests

    def test_get_action_list_with_superuser(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('admin_core:admin_action:action-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(u"Teszt akció" in response.content.decode('utf8'))
        self.assertTrue(u"Új Akció" in response.content.decode('utf8'))

    def test_get_action_list_without_superuser(self):
        # Bejelentkezés nélkül
        response = self.client.get(reverse('admin_core:admin_action:action-list'))
        self.assertEqual(response.status_code, 302) # Ami azt jelenti, hogy továbbítva lett az eredetileg elérni kívánt oldalról.

        # Vásárló fiókkal bejelentkezve
        self.client.login(username='customer', password='customer')
        response = self.client.get(reverse('admin_core:admin_action:action-list'))
        self.assertEqual(response.status_code, 302)

    # DetailView tests

    def test_get_action_detail_with_superuser(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('admin_core:admin_action:action-detail', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Teszt akció módosítás")

    def test_get_action_detail_with_customer(self):
        # Bejelentkezés nélkül
        response = self.client.get(reverse('admin_core:admin_action:action-detail', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 302)

        # Vásárló fiókkal bejelentkezve
        self.client.login(username='customer', password='customer')
        response = self.client.get(reverse('admin_core:admin_action:action-detail', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 302)

    def test_get_action_detail_404(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('admin_core:admin_action:action-detail', kwargs={'id': 5}))
        self.assertEqual(response.status_code, 404)

    # CreateView tests

    def test_get_action_create_with_superuser(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('admin_core:admin_action:action-create'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Akció létrehozás")

    def test_get_action_create_with_customer(self):
        # Bejelentkezés nélkül
        response = self.client.get(reverse('admin_core:admin_action:action-create'))
        self.assertEqual(response.status_code, 302)

        # Vásárló fiókkal bejelentkezve
        self.client.login(username='customer', password='customer')
        response = self.client.get(reverse('admin_core:admin_action:action-create'))
        self.assertEqual(response.status_code, 302)

    # DeleteView tests

    def test_get_action_delete_with_superuser(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('admin_core:admin_action:action-delete', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Teszt akció megnevezésű akciót")

    def test_get_action_delete_with_customer(self):
        # Bejelentkezés nélkül
        response = self.client.get(reverse('admin_core:admin_action:action-delete', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 302)

        # Vásárló fiókkal bejelentkezve
        self.client.login(username='customer', password='customer')
        response = self.client.get(reverse('admin_core:admin_action:action-delete', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 302)

    def test_get_action_delete_404(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('admin_core:admin_action:action-delete', kwargs={'id': 5}))
        self.assertEqual(response.status_code, 404)

# Form tests

class ActionFormTest(TestCase):
    def test_action_form(self):
        # Kötelező mezők teszt
        empty_data = {
            'name': '',
            'percent': '',
            'from_date': '',
            'to_date': '',
        }
        form = ActionForm(data=empty_data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)
        self.assertTrue('name' in form.errors and 'percent' in form.errors and 'from_date' in form.errors and 'to_date' in form.errors)

        # Negatív százalék teszt
        negative_percent_data = {
            'name': 'Teszt Akció',
            'percent': -10,
            'from_date': date.today(),
            'to_date': date.today() + timedelta(days=7),
        }
        form = ActionForm(data=negative_percent_data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)
        self.assertTrue('percent' in form.errors)

        # Túl nagy százalék teszt
        big_percent_data = {
            'name': 'Teszt Akció',
            'percent': 110,
            'from_date': date.today(),
            'to_date': date.today() + timedelta(days=7),
        }
        form = ActionForm(data=big_percent_data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)
        self.assertTrue('percent' in form.errors)

        # Helyes teszt
        valid_data = {
            'name': 'Teszt Akció',
            'percent': 50,
            'from_date': date.today(),
            'to_date': date.today() + timedelta(days=7),
        }
        form = ActionForm(data=valid_data)
        self.assertTrue(form.is_valid())
        self.assertTrue(not form.errors)

# Model tests

class ActionModelTest(TestCase):
    def test_action_model(self):
        action = Action.objects.create(
            id=5,
            name="Teszt akció",
            percent=30,
            from_date=date.today(),
            to_date=date.today() + timedelta(days=7)
        )

        self.assertEqual(str(action), action.name)
        self.assertIn(str(action.id), action.get_absolute_url())
        self.assertNotIn('1', action.get_absolute_url())