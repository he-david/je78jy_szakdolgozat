from django.test import TestCase
from django.test.client import Client
from django.shortcuts import reverse
from django.contrib.auth import get_user_model

from webshop.core.models import CustomUser, Contact, FAQTopic, FAQ
from administration.crm.forms import ContactForm, FaqTopicForm, FaqForm

User = get_user_model()

# Partner tests

    # View tests

class PartnerViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        User.objects.create_user(
            username='customer',
            email='customer@test.com',
            password='customer'
        )
        self.user = User.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='admin'
        )

    @classmethod
    def setUpTestData(cls):
        CustomUser.objects.create(
            is_staff=False,
            email='test@test.com',
            first_name='Jakab',
            last_name='Teszt' 
        )

    # ListView tests

    def test_get_partner_list_with_superuser(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('admin_core:crm:admin-partner-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(u"Teszt Jakab" in response.content.decode('utf8'))
        self.assertTrue(u"test@test.com" in response.content.decode('utf8'))

    def test_get_partner_list_without_superuser(self):
        # Bejelentkezés nélkül
        response = self.client.get(reverse('admin_core:crm:admin-partner-list'))
        self.assertEqual(response.status_code, 302)

        # Vásárló fiókkal bejelentkezve
        self.client.login(username='customer', password='customer')
        response = self.client.get(reverse('admin_core:crm:admin-partner-list'))
        self.assertEqual(response.status_code, 302)

# Contact tests

    # Views tests

class ContactViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        User.objects.create_user(
            username='customer',
            email='customer@test.com',
            password='customer'
        )
        self.user = User.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='admin'
        )

    @classmethod
    def setUpTestData(cls):
        Contact.objects.create(
            id=1,
            first_name='Jakab',
            last_name='Teszt',
            email='jakab@teszt.com',
            message='Ez egy teszt üzenet. Ez egy teszt üzenet.' 
        )
        Contact.objects.create(
            id=3,
            first_name='Elemér',
            last_name='Teszt',
            email='elemer@teszt.com',
            message='Ez egy rövid teszt üzenet.' 
        )

    # ListView tests

    def test_get_contact_list_with_superuser(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('admin_core:crm:message-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(u"Ez egy teszt üzenet. Ez egy te..." in response.content.decode('utf8')) # 30 karakternél hosszabb üzenet levágva
        self.assertTrue(u"Teszt Jakab" in response.content.decode('utf8'))
        self.assertTrue(u"jakab@teszt.com" in response.content.decode('utf8'))

        self.assertTrue(u"Ez egy rövid teszt üzenet." in response.content.decode('utf8'))

    def test_get_contact_list_without_superuser(self):
        # Bejelentkezés nélkül
        response = self.client.get(reverse('admin_core:crm:message-list'))
        self.assertEqual(response.status_code, 302)

        # Vásárló fiókkal bejelentkezve
        self.client.login(username='customer', password='customer')
        response = self.client.get(reverse('admin_core:crm:message-list'))
        self.assertEqual(response.status_code, 302)

    # DetailView tests

    def test_get_contact_detail_with_superuser(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('admin_core:crm:message-detail', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Üzenet módosítás")
        self.assertContains(response, "jakab@teszt.com")

        response = self.client.get(reverse('admin_core:crm:message-detail', kwargs={'id': 3}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Üzenet módosítás")
        self.assertContains(response, "elemer@teszt.com")

    def test_get_contact_detail_with_customer(self):
        # Bejelentkezés nélkül
        response = self.client.get(reverse('admin_core:crm:message-detail', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 302)

        # Vásárló fiókkal bejelentkezve
        self.client.login(username='customer', password='customer')
        response = self.client.get(reverse('admin_core:crm:message-detail', kwargs={'id': 3}))
        self.assertEqual(response.status_code, 302)

    def test_get_contact_detail_404(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('admin_core:crm:message-detail', kwargs={'id': 2}))
        self.assertEqual(response.status_code, 404)

    # DeleteView tests

    def test_get_contact_delete_with_superuser(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('admin_core:crm:message-delete', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "jakab@teszt.com e-maillel")

        response = self.client.get(reverse('admin_core:crm:message-delete', kwargs={'id': 3}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "elemer@teszt.com e-maillel")

    def test_get_contact_delete_with_customer(self):
        # Bejelentkezés nélkül
        response = self.client.get(reverse('admin_core:crm:message-delete', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 302)

        # Vásárló fiókkal bejelentkezve
        self.client.login(username='customer', password='customer')
        response = self.client.get(reverse('admin_core:crm:message-delete', kwargs={'id': 3}))
        self.assertEqual(response.status_code, 302)

    def test_get_contact_delete_404(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('admin_core:crm:message-delete', kwargs={'id': 2}))
        self.assertEqual(response.status_code, 404)

    # Form tests

class ContactFormTest(TestCase):

    def test_contact_form(self):
        # Kötelező mezők teszt
        empty_data = {
            'first_name': '',
            'last_name': '',
            'email': '',
            'message': ''
        }
        form = ContactForm(data=empty_data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)
        self.assertTrue('first_name' in form.errors and 'last_name' in form.errors and 'email' in form.errors and 'message' in form.errors)

        # Hosszú nevek teszt
        long_name_data = {
            'first_name': 'TesztTesztTesztTesztTesztTesztTesztTesztTesztTesztTeszt',
            'last_name': 'TesztTesztTesztTesztTesztTesztTesztTesztTesztTesztTeszt',
            'email': 'teszt@teszt.com',
            'message': 'Ez egy teszt üzenet.'
        }
        form = ContactForm(data=long_name_data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)
        self.assertTrue('first_name' in form.errors and 'last_name' in form.errors)

    # Model tests

class ContactModelTest(TestCase):

    def test_contact_model(self):
        message = Contact.objects.create(
            id=1,
            first_name='Jakab',
            last_name='Teszt',
            email='jakab@teszt.com',
            message='Ez egy teszt üzenet. Ez egy teszt üzenet.' 
        )

        self.assertEqual(str(message), message.email)
        self.assertIn(str(message.id), message.get_absolute_url())
        self.assertNotIn('2', message.get_absolute_url())

# FAQ Topic tests

    # Views tests

class FaqTopicViewTest(TestCase):
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
        FAQTopic.objects.create(
            id=11,
            name='Teszt téma'
        )
    
    # ListView tests

    def test_get_faq_topic_list_with_superuser(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('admin_core:crm:faq-topic-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(u"Teszt téma" in response.content.decode('utf8'))
        self.assertTrue(u"Új Témakör" in response.content.decode('utf8'))

    def test_get_faq_topic_list_without_superuser(self):
        # Bejelentkezés nélkül
        response = self.client.get(reverse('admin_core:crm:faq-topic-list'))
        self.assertEqual(response.status_code, 302)

        # Vásárló fiókkal bejelentkezve
        self.client.login(username='customer', password='customer')
        response = self.client.get(reverse('admin_core:crm:faq-topic-list'))
        self.assertEqual(response.status_code, 302)

    # DetailView tests

    def test_get_faq_topic_detail_with_superuser(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('admin_core:crm:faq-topic-detail', kwargs={'id': 11}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Teszt téma módosítás")

    def test_get_faq_topic_detail_with_customer(self):
        # Bejelentkezés nélkül
        response = self.client.get(reverse('admin_core:crm:faq-topic-detail', kwargs={'id': 11}))
        self.assertEqual(response.status_code, 302)

        # Vásárló fiókkal bejelentkezve
        self.client.login(username='customer', password='customer')
        response = self.client.get(reverse('admin_core:crm:faq-topic-detail', kwargs={'id': 11}))
        self.assertEqual(response.status_code, 302)

    def test_get_faq_topic_detail_404(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('admin_core:crm:faq-topic-detail', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 404)

    # CreateView tests

    def test_get_faq_topic_create_with_superuser(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('admin_core:crm:faq-topic-create'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "GY.I.K. Témakör létrehozás")

    def test_get_faq_topic_create_with_customer(self):
        # Bejelentkezés nélkül
        response = self.client.get(reverse('admin_core:crm:faq-topic-create'))
        self.assertEqual(response.status_code, 302)

        # Vásárló fiókkal bejelentkezve
        self.client.login(username='customer', password='customer')
        response = self.client.get(reverse('admin_core:crm:faq-topic-create'))
        self.assertEqual(response.status_code, 302)

    # DeleteView tests

    def test_get_faq_topic_delete_with_superuser(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('admin_core:crm:faq-topic-delete', kwargs={'id': 11}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Teszt téma nevű témakört")

    def test_get_faq_topic_delete_with_customer(self):
        # Bejelentkezés nélkül
        response = self.client.get(reverse('admin_core:crm:faq-topic-delete', kwargs={'id': 11}))
        self.assertEqual(response.status_code, 302)

        # Vásárló fiókkal bejelentkezve
        self.client.login(username='customer', password='customer')
        response = self.client.get(reverse('admin_core:crm:faq-topic-delete', kwargs={'id': 11}))
        self.assertEqual(response.status_code, 302)

    def test_get_faq_topic_delete_404(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('admin_core:crm:faq-topic-delete', kwargs={'id': 2}))
        self.assertEqual(response.status_code, 404)

    # Form tests

class FaqTopicFormTest(TestCase):

    def test_faq_topic_form(self):
        # Kötelező mezők teszt
        empty_data = {
            'name': '',
        }
        form = FaqTopicForm(data=empty_data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)
        self.assertTrue('name' in form.errors)

        # Hosszú név teszt
        long_name_data = {
            'name': 'TesztTesztTesztTesztTesztTesztTesztTesztTesztTesztTeszt',
        }
        form = FaqTopicForm(data=long_name_data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)
        self.assertTrue('name' in form.errors)

        # Helyes teszt
        valid_data = {
            'name': 'Teszt téma',
        }
        form = FaqTopicForm(data=valid_data)
        self.assertTrue(form.is_valid())
        self.assertTrue(not form.errors)

    # Model tests

class FaqTopicModelTest(TestCase):

    def test_faq_topic_model(self):
        topic = FAQTopic.objects.create(
            id=5,
            name='Teszt téma'
        )

        self.assertEqual(str(topic), topic.name)
        self.assertIn(str(topic.id), topic.get_absolute_url())
        self.assertNotIn('1', topic.get_absolute_url())

# FAQ tests

    # Views tests

class FaqViewTest(TestCase):
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
        FAQ.objects.create(
            id=3,
            question='Ez egy teszt kérdés',
            answer='Ez egy teszt válasz',
            topic_id = FAQTopic.objects.create(name='Teszt téma')
        )
    
    # ListView tests

    def test_get_faq_list_with_superuser(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('admin_core:crm:faq-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(u"Ez egy teszt kérdés" in response.content.decode('utf8'))
        self.assertTrue(u"Új GY.I.K." in response.content.decode('utf8'))

    def test_get_faq_list_without_superuser(self):
        # Bejelentkezés nélkül
        response = self.client.get(reverse('admin_core:crm:faq-list'))
        self.assertEqual(response.status_code, 302)

        # Vásárló fiókkal bejelentkezve
        self.client.login(username='customer', password='customer')
        response = self.client.get(reverse('admin_core:crm:faq-list'))
        self.assertEqual(response.status_code, 302)

    # DetailView tests

    def test_get_faq_detail_with_superuser(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('admin_core:crm:faq-detail', kwargs={'id': 3}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "GY.I.K. módosítás")

    def test_get_faq_detail_with_customer(self):
        # Bejelentkezés nélkül
        response = self.client.get(reverse('admin_core:crm:faq-detail', kwargs={'id': 3}))
        self.assertEqual(response.status_code, 302)

        # Vásárló fiókkal bejelentkezve
        self.client.login(username='customer', password='customer')
        response = self.client.get(reverse('admin_core:crm:faq-detail', kwargs={'id': 3}))
        self.assertEqual(response.status_code, 302)

    def test_get_faq_detail_404(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('admin_core:crm:faq-detail', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 404)

    # CreateView tests

    def test_get_faq_create_with_superuser(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('admin_core:crm:faq-create'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "GY.I.K. létrehozás")

    def test_get_faq_create_with_customer(self):
        # Bejelentkezés nélkül
        response = self.client.get(reverse('admin_core:crm:faq-create'))
        self.assertEqual(response.status_code, 302)

        # Vásárló fiókkal bejelentkezve
        self.client.login(username='customer', password='customer')
        response = self.client.get(reverse('admin_core:crm:faq-create'))
        self.assertEqual(response.status_code, 302)

    # DeleteView tests

    def test_get_faq_delete_with_superuser(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('admin_core:crm:faq-delete', kwargs={'id': 3}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Biztosan törölni szeretné")

    def test_get_faq_delete_with_customer(self):
        # Bejelentkezés nélkül
        response = self.client.get(reverse('admin_core:crm:faq-delete', kwargs={'id': 3}))
        self.assertEqual(response.status_code, 302)

        # Vásárló fiókkal bejelentkezve
        self.client.login(username='customer', password='customer')
        response = self.client.get(reverse('admin_core:crm:faq-delete', kwargs={'id': 3}))
        self.assertEqual(response.status_code, 302)

    def test_get_faq_delete_404(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('admin_core:crm:faq-delete', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 404)

    # Form tests

class FaqFormTest(TestCase):

    def test_faq_form(self):
        topic = FAQTopic.objects.create(
            name='Teszt téma'
        )
        # Kötelező mezők teszt
        empty_data = {
            'question': '',
            'answer': '',
            'topic_id': '',
        }
        form = FaqForm(data=empty_data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)
        self.assertTrue('question' in form.errors and 'answer' in form.errors and 'topic_id' in form.errors)

        # Hosszú név teszt
        long_question_data = {
            'question': 'x'*201,
            'answer': 'Teszt válasz',
            'topic_id': topic,
        }
        form = FaqForm(data=long_question_data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)
        self.assertTrue('question' in form.errors)

        # Helyes teszt
        valid_data = {
            'question': 'Teszt kérdés',
            'answer': 'Teszt válasz',
            'topic_id': topic,
        }
        form = FaqForm(data=valid_data)
        self.assertTrue(form.is_valid())
        self.assertTrue(not form.errors)

    # Model tests

class FaqModelTest(TestCase):

    def test_faq_model(self):
        topic = FAQTopic.objects.create(
            name='Teszt téma'
        )
        faq = FAQ.objects.create(
            id=5,
            question='Ez az első teszt kérdés',
            answer='Ez az első teszt válasz',
            topic_id=topic
        )
        faq2 = FAQ.objects.create(
            id=6,
            question='Ez a második teszt kérdés',
            answer='Ez a második teszt válasz',
            topic_id=topic
        )

        self.assertEqual(str(faq), faq.question)
        self.assertIn(str(faq.id), faq.get_absolute_url())
        self.assertNotIn('1', faq.get_absolute_url())
        self.assertTrue(faq.is_visible_category())
        self.assertFalse(faq2.is_visible_category())