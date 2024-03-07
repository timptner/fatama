from django.contrib.auth.models import User
from django.test import TestCase

from accounts.forms import CouncilForm, InviteForm, ProfileForm, SetPasswordForm, UserForm


class CouncilFormTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username='john')

    def test_form(self) -> None:
        data = {
            'university': 'Otto-von-Guericke-Universität Magdeburg',
            'name': 'Fachschaftsrat Maschinenbau',
        }
        form = CouncilForm(data=data, user=self.user)
        self.assertTrue(form.is_valid())


class InviteFormTest(TestCase):
    def test_form_valid(self) -> None:
        data = {
            'emails': 'john.doe@example.org, jane.doe@example.org',
        }
        form = InviteForm(data=data, user=None)
        self.assertTrue(form.is_valid())

    def test_form_invalid(self) -> None:
        data = {
            'emails': 'john.doe, jane.doe@example.org',
        }
        form = InviteForm(data=data, user=None)
        self.assertFalse(form.is_valid())


class ProfileFormTest(TestCase):
    def test_form_valid(self) -> None:
        data = {}
        form = ProfileForm(data=data, user=None)
        self.assertTrue(form.is_valid())


class SetPasswordFormTest(TestCase):
    def test_form_valid(self) -> None:
        data = {
            'new_password1': 'super53cre7',
            'new_password2': 'super53cre7',
        }
        form = SetPasswordForm(data=data, user=None)
        self.assertTrue(form.is_valid())


class UserFormTest(TestCase):
    def test_form_valid(self) -> None:
        data = {
            'username': 'john',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.org',
        }
        form = UserForm(data=data)
        self.assertTrue(form.is_valid())
