from django.test import TestCase
from django.test.client import Client
from django.shortcuts import reverse
from django.contrib.auth import get_user_model

from webshop.product.models import Category, Product
from administration.category.forms import CategoryForm, CategoryCreateForm

User = get_user_model()

# Views tests

class CategoryViewTest(TestCase):
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
        cat = Category.objects.create(
            id=1,
            name="Teszt szülő kategória",
            parent_id=None
        )
        Category.objects.create(
            id=2,
            name="Teszt gyerek kategória",
            parent_id=cat
        )

    # ListView tests

    def test_get_category_list_with_superuser(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('admin_core:admin_category:category-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(u"Teszt szülő kategória" in response.content.decode('utf8'))
        self.assertTrue(u"Új Kategória" in response.content.decode('utf8'))

    def test_get_category_list_without_superuser(self):
        # Bejelentkezés nélkül
        response = self.client.get(reverse('admin_core:admin_category:category-list'))
        self.assertEqual(response.status_code, 302)

        # Vásárló fiókkal bejelentkezve
        self.client.login(username='customer', password='customer')
        response = self.client.get(reverse('admin_core:admin_category:category-list'))
        self.assertEqual(response.status_code, 302)

    # DetailView tests

    def test_get_category_detail_with_superuser(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('admin_core:admin_category:category-detail', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Teszt szülő kategória módosítás")
        self.assertContains(response, "Az adott kategóriához nem tartozik egyetlen termék sem.")

    def test_get_category_detail_with_customer(self):
        # Bejelentkezés nélkül
        response = self.client.get(reverse('admin_core:admin_category:category-detail', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 302)

        # Vásárló fiókkal bejelentkezve
        self.client.login(username='customer', password='customer')
        response = self.client.get(reverse('admin_core:admin_category:category-detail', kwargs={'id': 2}))
        self.assertEqual(response.status_code, 302)

    def test_get_category_detail_404(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('admin_core:admin_category:category-detail', kwargs={'id': 5}))
        self.assertEqual(response.status_code, 404)

    # CreateView tests

    def test_get_category_create_with_superuser(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('admin_core:admin_category:category-create'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Kategória létrehozás")

    def test_get_category_create_with_customer(self):
        # Bejelentkezés nélkül
        response = self.client.get(reverse('admin_core:admin_category:category-create'))
        self.assertEqual(response.status_code, 302)

        # Vásárló fiókkal bejelentkezve
        self.client.login(username='customer', password='customer')
        response = self.client.get(reverse('admin_core:admin_category:category-create'))
        self.assertEqual(response.status_code, 302)

    # DeleteView tests

    def test_get_category_delete_with_superuser(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('admin_core:admin_category:category-delete', kwargs={'id': 2}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Teszt gyerek kategória nevű kategóriát")

    def test_get_category_delete_with_customer(self):
        # Bejelentkezés nélkül
        response = self.client.get(reverse('admin_core:admin_category:category-delete', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 302)

        # Vásárló fiókkal bejelentkezve
        self.client.login(username='customer', password='customer')
        response = self.client.get(reverse('admin_core:admin_category:category-delete', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 302)

    def test_get_category_delete_404(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('admin_core:admin_category:category-delete', kwargs={'id': 3}))
        self.assertEqual(response.status_code, 404)

# Forms tests

class CategoryFormTest(TestCase):
    
    def test_category_form(self):
        # Kötelező mezők teszt
        empty_data = {
            'name': '',
        }
        form = CategoryForm(data=empty_data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)
        self.assertTrue('name' in form.errors)

        # Negatív százalék teszt
        long_name_data = {
            'name': 'x'*101,
        }
        form = CategoryForm(data=long_name_data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)
        self.assertTrue('name' in form.errors)

        # Helyes teszt
        valid_data = {
            'name': 'Teszt Kategória',
        }
        form = CategoryForm(data=valid_data)
        self.assertTrue(form.is_valid())
        self.assertTrue(not form.errors)

    def test_category_create_form(self):
        # Kötelező mezők teszt
        empty_data = {
            'name': '',
        }
        form = CategoryCreateForm(data=empty_data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)
        self.assertTrue('name' in form.errors)

        # Hosszú név teszt
        long_name_data = {
            'name': 'x'*101,
        }
        form = CategoryCreateForm(data=long_name_data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)
        self.assertTrue('name' in form.errors)

        # Helyes teszt
        valid_data = {
            'name': 'Teszt Kategória',
        }
        form = CategoryCreateForm(data=valid_data)
        self.assertTrue(form.is_valid())
        self.assertTrue(not form.errors)

# Model tests

class CategoryModelTest(TestCase):
    
    def test_category_model(self):
        category = Category.objects.create(
            id=5,
            name="Teszt Kategória",
        )

        self.assertEqual(str(category), category.name)
        self.assertIn(str(category.id), category.get_absolute_admin_url())
        self.assertNotIn('4', category.get_absolute_admin_url())
        self.assertEqual(0, category.get_product_count())

        Product.objects.create(
            name='Teszt',
            producer='Teszt Gyártó',
            vat=27,
            category_id=category,
        )
        self.assertEqual(1, category.get_product_count())