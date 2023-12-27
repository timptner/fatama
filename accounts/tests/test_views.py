import secrets

from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import User, Permission
from django.contrib.auth.tokens import default_token_generator
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from accounts.models import Invite


class InviteViewTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user('john')
        can_invite = Permission.objects.get(codename='can_invite')
        self.user.user_permissions.add(can_invite)
        self.path = reverse('accounts:create_invite')

    def test_view(self) -> None:
        response = self.client.get(self.path)
        path = reverse('accounts:login')
        self.assertRedirects(response, f"{path}?next={self.path}")

    def test_user_view(self) -> None:
        self.client.force_login(self.user)
        response = self.client.get(self.path)
        self.assertContains(response, "Einladung erstellen")


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


class PasswortResetView(TestCase):
    def setUp(self) -> None:
        self.path = reverse('accounts:password_reset')
        self.user = User.objects.create_user(
            username='john',
            email='john.doe@example.org',
            first_name='John',
        )

    def test_get_view(self) -> None:
        response = self.client.get(self.path)
        self.assertContains(response, "Passwort zurücksetzen")

    def test_post_view(self) -> None:
        data = {
            'email': self.user.email,
        }
        response = self.client.post(self.path, data)
        self.assertRedirects(response, reverse('accounts:login'))


class PasswortResetConfirmView(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username='john')
        self.kwargs = {
            'uidb64': urlsafe_base64_encode(force_bytes(self.user.pk)),
            'token': default_token_generator.make_token(self.user),
        }
        self.path = reverse('accounts:password_reset_confirm', kwargs=self.kwargs)

    def test_get_view(self) -> None:
        response = self.client.get(self.path)
        self.kwargs.update({'token': 'set-password'})
        next_path = reverse('accounts:password_reset_confirm', kwargs=self.kwargs)
        self.assertRedirects(response, next_path)


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
