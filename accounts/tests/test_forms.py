from django.test import TestCase

from accounts.forms import RegistrationForm


class RegistrationFormTest(TestCase):
    def test_form_valid(self) -> None:
        data = {
            'username': 'john',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.org',
            'password1': 'super53cre7',
            'password2': 'super53cre7',
        }
        form = RegistrationForm(data=data)
        self.assertTrue(form.is_valid())
