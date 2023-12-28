from django.test import TestCase
from django.contrib.auth.models import User

from congresses.forms import ParticipantForm
from congresses.models import Congress


class ParticipantFormTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username='john')
        self.congress = Congress.objects.create(title="FaTaMa 2024", location="Magdeburg")

    def test_form(self) -> None:
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
        }
        form = ParticipantForm(data=data, congress=self.congress, user=self.user)
        self.assertTrue(form.is_valid())
