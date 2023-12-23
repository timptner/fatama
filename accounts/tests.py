from django.test import TestCase
from django.urls import reverse


class ProfileViewTest(TestCase):
    def test_view(self) -> None:
        response = self.client.get(reverse('accounts:profile'))
        self.assertContains(response, 'Profil')
