from django.test import TestCase

from accounts.forms import ProfileForm, SetPasswordForm, UserForm


class ProfileFormTest(TestCase):
    def test_form_valid(self) -> None:
        data = {
            'university': 'Otto-von-Guericke-Universität Magdeburg',
        }
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
