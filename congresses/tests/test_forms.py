from django.test import TestCase
from django.contrib.auth.models import User

from congresses.forms import ParticipantForm, PortraitForm
from congresses.models import Congress, Participant, Portrait


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


class PortraitFormTest(TestCase):
    def setUp(self) -> None:
        congress = Congress.objects.create(title='FaTaMa 2024', location='Magdeburg')
        self.participant = Participant.objects.create(congress=congress, first_name='John', last_name='Doe')

    def test_form(self) -> None:
        data = {
            'diet': Portrait.VEGAN,
            'intolerances': '',
            'railcard': Portrait.GERMANY_TICKET,
        }
        form = PortraitForm(data=data, participant=self.participant)
        self.assertTrue(form.is_valid())
