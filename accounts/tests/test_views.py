import secrets

from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from accounts.models import Invite


class InviteViewTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user('john')
        self.path = reverse('accounts:create_invite')

    def test_view(self) -> None:
        response = self.client.get(self.path)
        path = reverse('accounts:login')
        self.assertRedirects(response, f"{path}?next={self.path}")

    def test_user_view(self) -> None:
        self.client.force_login(self.user)
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 403)


class LoginViewTest(TestCase):
    def setUp(self) -> None:
        self.path = reverse('accounts:login')

    def test_view(self) -> None:
        response = self.client.get(self.path)
        self.assertContains(response, "Anmelden")


class LogoutView(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user('john')
        self.path = reverse('accounts:logout')

    def test_get_view(self) -> None:
        response = self.client.get(self.path)
        self.assertRedirects(response, reverse('accounts:login'))

    def test_user_get_view(self) -> None:
        self.client.force_login(self.user)
        response = self.client.get(self.path)
        self.assertContains(response, "Abmelden")

    def test_post_view(self) -> None:
        response = self.client.post(self.path)
        self.assertRedirects(response, reverse('accounts:login'))


class ProfileViewTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user('john')
        self.path = reverse('accounts:profile')

    def test_view(self) -> None:
        response = self.client.get(self.path)
        path = reverse('accounts:login')
        self.assertRedirects(response, f'{path}?next={self.path}')

    def test_user_view(self) -> None:
        self.client.force_login(self.user)
        response = self.client.get(self.path)
        self.assertContains(response, 'Profil')


class RegistrationViewTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user('john')
        token = secrets.token_urlsafe(settings.INVITE_TOKEN_LENGTH)
        expired_at = timezone.now() + timedelta(days=settings.INVITE_EXPIRATION)
        self.invite = Invite.objects.create(token=token, sender=self.user, expired_at=expired_at)
        self.path = reverse('accounts:register', kwargs={'token': self.invite.token})

    def test_get_view(self) -> None:
        response = self.client.get(self.path)
        self.assertContains(response, 'Registrieren')

    def test_post_view(self) -> None:
        data = {
            'profile-university': 'Otto-von-Guericke-University Magdeburg',
            'user-username': 'jane',
            'user-first_name': 'Jane',
            'user-last_name': 'Doe',
            'user-email': 'jane.doe@example.org',
            'password-new_password1': 'super53cre7',
            'password-new_password2': 'super53cre7',
        }
        response = self.client.post(self.path, data=data)
        self.assertRedirects(response, reverse('accounts:login'))
