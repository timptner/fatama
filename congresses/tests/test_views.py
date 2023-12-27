from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class CongressListView(TestCase):
    def setUp(self) -> None:
        self.path = reverse('congresses:congress_list')
        self.user = User.objects.create_user(username='john')

    def test_view(self) -> None:
        response = self.client.get(self.path)
        path = reverse('accounts:login')
        self.assertRedirects(response, f'{path}?next={self.path}')

    def test_user_view(self) -> None:
        self.client.force_login(self.user)
        response = self.client.get(self.path)
        self.assertContains(response, "Tagungen")
