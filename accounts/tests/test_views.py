import logging
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
from congresses.models import Congress


class CouncilCreateViewTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username='john')
        self.path = reverse('accounts:create_council')

    def test_public_view(self) -> None:
        response = self.client.get(self.path)
        path = reverse('accounts:login')
        self.assertRedirects(response, f'{path}?next={self.path}')

    def test_public_form_view(self) -> None:
        response = self.client.post(self.path)
        path = reverse('accounts:login')
        self.assertRedirects(response, f'{path}?next={self.path}')

    def test_user_view(self) -> None:
        self.client.force_login(self.user)
        response = self.client.get(self.path)
        self.assertContains(response, 'Gremium registrieren')

    def test_user_form_view(self) -> None:
        data = {
            'university': 'Otto-von-Guericke-Universität Magdeburg',
            'name': 'Fachschaftsrat Maschinenbau',
        }
        self.client.force_login(self.user)
        response = self.client.post(self.path, data=data)
        self.assertRedirects(response, reverse('accounts:council_list'))


class CouncilListViewTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username='john')
        self.path = reverse('accounts:council_list')

    def test_public_view(self) -> None:
        response = self.client.get(self.path)
        path = reverse('accounts:login')
        self.assertRedirects(response, f"{path}?next={self.path}")

    def test_user_view(self) -> None:
        self.client.force_login(self.user)
        response = self.client.get(self.path)
        self.assertContains(response, "Verzeichnis aller Gremien")


class InviteCreateViewTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user('john')
        can_invite = Permission.objects.get(codename='can_invite')
        self.user.user_permissions.add(can_invite)
        self.path = reverse('accounts:create_invite')

    def test_public_view(self) -> None:
        response = self.client.get(self.path)
        path = reverse('accounts:login')
        self.assertRedirects(response, f"{path}?next={self.path}")

    def test_public_form_view(self) -> None:
        response = self.client.post(self.path)
        path = reverse('accounts:login')
        self.assertRedirects(response, f'{path}?next={self.path}')

    def test_user_view(self) -> None:
        self.client.force_login(self.user)
        response = self.client.get(self.path)
        self.assertContains(response, "Einladung erstellen")

    def test_user_form_view(self) -> None:
        data = {
            'emails': 'john.doe@example.org, jane.doe@example.org',
        }
        self.client.force_login(self.user)
        response = self.client.post(self.path, data=data)
        self.assertRedirects(response, reverse('accounts:create_invite'))


class LoginViewTest(TestCase):
    def setUp(self) -> None:
        self.path = reverse('accounts:login')

    def test_public_view(self) -> None:
        response = self.client.get(self.path)
        self.assertContains(response, "Anmelden")


class LogoutViewTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username='john')
        self.path = reverse('accounts:logout')

    def test_public_view(self) -> None:
        response = self.client.get(self.path)
        self.assertRedirects(response, reverse('accounts:login'))

    def test_public_form_view(self) -> None:
        response = self.client.post(self.path)
        self.assertRedirects(response, reverse('accounts:login'))

    def test_user_view(self) -> None:
        self.client.force_login(self.user)
        response = self.client.get(self.path)
        self.assertContains(response, "Abmelden")

    def test_user_form_view(self) -> None:
        self.client.force_login(self.user)
        response = self.client.post(self.path)
        self.assertRedirects(response, reverse('accounts:login'))
        self.assertIsNone(self.client.session.__dict__['_SessionBase__session_key'])


class PasswordResetViewTest(TestCase):
    def setUp(self) -> None:
        self.path = reverse('accounts:password_reset')
        self.user = User.objects.create_user(
            username='john',
            email='john.doe@example.org',
            first_name='John',
        )

    def test_public_view(self) -> None:
        response = self.client.get(self.path)
        self.assertContains(response, "Passwort zurücksetzen")

    def test_public_form_view(self) -> None:
        data = {
            'email': self.user.email,
        }
        response = self.client.post(self.path, data)
        self.assertRedirects(response, reverse('accounts:login'))


class PasswordChangeViewTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username='john', password='secret123')
        self.path = reverse('accounts:edit_password')

    def test_public_viw(self) -> None:
        response = self.client.get(self.path)
        path = reverse('accounts:login')
        self.assertRedirects(response, f'{path}?next={self.path}')

    def test_public_form_view(self) -> None:
        response = self.client.post(self.path)
        path = reverse('accounts:login')
        self.assertRedirects(response, f'{path}?next={self.path}')

    def test_user_view(self) -> None:
        self.client.force_login(self.user)
        response = self.client.get(self.path)
        self.assertContains(response, "Passwort ändern")

    def test_user_form_view(self) -> None:
        self.client.force_login(self.user)
        data = {
            'old_password': 'secret123',
            'new_password1': '124secret',
            'new_password2': '124secret',
        }
        response = self.client.post(self.path, data=data)
        self.assertRedirects(response, reverse('accounts:edit_password'))


class PasswordResetConfirmViewTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username='john')
        self.kwargs = {
            'uidb64': urlsafe_base64_encode(force_bytes(self.user.pk)),
            'token': default_token_generator.make_token(self.user),
        }
        self.path = reverse('accounts:password_reset_confirm', kwargs=self.kwargs)

    def test_public_view(self) -> None:
        response = self.client.get(self.path)
        self.kwargs.update({'token': 'set-password'})
        next_path = reverse('accounts:password_reset_confirm', kwargs=self.kwargs)
        self.assertRedirects(response, next_path)


class ProfileViewTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user('john')
        self.path = reverse('accounts:profile')

    def test_public_view(self) -> None:
        response = self.client.get(self.path)
        path = reverse('accounts:login')
        self.assertRedirects(response, f'{path}?next={self.path}')

    def test_user_view(self) -> None:
        self.client.force_login(self.user)
        response = self.client.get(self.path)
        self.assertContains(response, 'Profil')


class RegistrationViewTest(TestCase):
    def setUp(self) -> None:
        logging.disable(logging.WARNING)
        self.user = User.objects.create_user('john')
        self.data = {
            'user-username': 'jane',
            'user-first_name': 'Jane',
            'user-last_name': 'Doe',
            'user-email': 'jane.doe@example.org',
            'password-new_password1': 'super53cre7',
            'password-new_password2': 'super53cre7',
        }

    def _get_valid_token(self) -> str:
        token = secrets.token_urlsafe(settings.INVITE_TOKEN_LENGTH)
        expired_at = timezone.now() + timedelta(days=settings.INVITE_EXPIRATION)
        invite = Invite.objects.create(token=token, sender=self.user, expired_at=expired_at)
        return invite.token

    def _get_expired_token(self) -> str:
        token = secrets.token_urlsafe(settings.INVITE_TOKEN_LENGTH)
        expired_at = timezone.now() - timedelta(hours=1)
        invite = Invite.objects.create(token=token, sender=self.user, expired_at=expired_at)
        return invite.token

    def test_public_view(self) -> None:
        token = self._get_valid_token()
        path = reverse('accounts:register', kwargs={'token': token})
        response = self.client.get(path)
        self.assertContains(response, 'Registrieren')

    def test_valid_token(self) -> None:
        token = self._get_valid_token()
        path = reverse('accounts:register', kwargs={'token': token})
        response = self.client.post(path, data=self.data)
        self.assertRedirects(response, reverse('accounts:login'))

    def test_invalid_token(self) -> None:
        token = 'invalid'
        path = reverse('accounts:register', kwargs={'token': token})
        response = self.client.post(path, data=self.data)
        self.assertEqual(response.status_code, 404)

    def test_expired_token(self) -> None:
        token = self._get_expired_token()
        path = reverse('accounts:register', kwargs={'token': token})
        response = self.client.post(path, data=self.data)
        self.assertEqual(response.status_code, 403)


class UserUpdateViewTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user('john')
        self.data = {
            'username': 'jane',
            'first_name': 'Jane',
            'last_name': 'Doe',
            'email': 'jane.doe@example.org',
        }
        self.path = reverse('accounts:edit_profile')

    def test_public_view(self) -> None:
        response = self.client.get(self.path)
        path = reverse('accounts:login')
        self.assertRedirects(response, f'{path}?next={self.path}')

    def test_public_form_view(self) -> None:
        response = self.client.post(self.path, data=self.data)
        path = reverse('accounts:login')
        self.assertRedirects(response, f'{path}?next={self.path}')

    def test_user_view(self) -> None:
        self.client.force_login(self.user)
        response = self.client.get(self.path)
        self.assertContains(response, "Profil bearbeiten")

    def test_user_form_view(self) -> None:
        self.client.force_login(self.user)
        response = self.client.post(self.path, data=self.data)
        self.assertRedirects(response, reverse('accounts:profile'))
