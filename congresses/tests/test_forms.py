from django.test import TestCase
from django.contrib.auth.models import User

from accounts.models import Council
from congresses.forms import AttendanceForm, ParticipantForm, PortraitForm
from congresses.models import Attendance, Congress, Participant, Portrait


class AttendanceFormTest(TestCase):
    def setUp(self) -> None:
        self.congress = Congress.objects.create(title="FaTaMa 2024", location="Magdeburg")
        user = User.objects.create_user(username='john')
        self.council = Council.objects.create(
            owner=user,
            university="Otto-von-Guericke-Universität Magdeburg",
            name="Fachschaftsrat Maschinenbau",
        )

    def test_form(self) -> None:
        form = AttendanceForm(data={}, congress=self.congress, council=self.council)
        self.assertTrue(form.is_valid())


class ParticipantFormTest(TestCase):
    def setUp(self) -> None:
        user = User.objects.create_user(username='john')
        council = Council.objects.create(
            owner=user,
            university="Otto-von-Guericke-Universität Magdeburg",
            name="Fachschaftsrat Maschinenbau",
        )
        congress = Congress.objects.create(title="FaTaMa 2024", location="Magdeburg")
        self.attendance = Attendance.objects.create(council=council, congress=congress)

    def test_form(self) -> None:
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
        }
        form = ParticipantForm(data=data, attendance=self.attendance)
        self.assertTrue(form.is_valid())


class PortraitFormTest(TestCase):
    def setUp(self) -> None:
        user = User.objects.create(username='john')
        council = Council.objects.create(
            owner=user,
            university="Otto-von-Guericke-Universität Magdeburg",
            name="Fachschaftsrat Maschinenbau",
        )
        congress = Congress.objects.create(title='FaTaMa 2024', location='Magdeburg')
        attendance = Attendance.objects.create(council=council, congress=congress)
        self.participant = Participant.objects.create(attendance=attendance, first_name='John', last_name='Doe')

    def test_form(self) -> None:
        data = {
            'diet': Portrait.VEGAN,
            'intolerances': '',
            'railcard': Portrait.GERMANY_TICKET,
        }
        form = PortraitForm(data=data, participant=self.participant)
        self.assertTrue(form.is_valid())
