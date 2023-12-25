from django.test import TestCase
from django.urls import reverse


class InviteViewTest(TestCase):
    def test_view(self) -> None:
        url = reverse('accounts:create_invite')
        response = self.client.get(url)
        self.assertRedirects(response, f"{reverse('accounts:login')}?next={url}")


class LoginViewTest(TestCase):
    def test_view(self) -> None:
        response = self.client.get(reverse('accounts:login'))
        self.assertContains(response, "Anmelden")


class ProfileViewTest(TestCase):
    def test_view(self) -> None:
        response = self.client.get(reverse('accounts:profile'))
        self.assertContains(response, 'Profil')
