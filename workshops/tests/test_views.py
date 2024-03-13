from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class WorkshopCreateViewTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username='john')
        self.path = reverse('workshops:create_workshop')
        self.data = {
            "title": "Foo",
            "description": "Bar",
        }

    def test_public_view(self):
        response = self.client.get(self.path)
        path = reverse('accounts:login')
        self.assertRedirects(response, f'{path}?next={self.path}')

    def test_public_form_view(self):
        response = self.client.post(self.path, data=self.data)
        path = reverse('accounts:login')
        self.assertRedirects(response, f'{path}?next={self.path}')

    def test_user_view(self):
        self.client.force_login(self.user)
        response = self.client.get(self.path)
        self.assertContains(response, 'Seminar erstellen')

    def test_user_form_view(self):
        self.client.force_login(self.user)
        response = self.client.post(self.path, data=self.data)
        self.assertRedirects(response, reverse('workshops:workshop_list'))


class WorkshopListView(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username='john')
        self.path = reverse('workshops:workshop_list')

    def test_public_view(self) -> None:
        response = self.client.get(self.path)
        path = reverse('accounts:login')
        self.assertRedirects(response, f'{path}?next={self.path}')

    def test_user_view(self) -> None:
        self.client.force_login(self.user)
        response = self.client.get(self.path)
        self.assertContains(response, "Seminare")
