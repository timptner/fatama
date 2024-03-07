from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

from accounts.models import Council
from congresses.forms import AttendanceForm, ParticipantForm, PortraitForm, SeatForm
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
            'size': Portrait.MEDIUM,
            'railcard': Portrait.STUDENT_CARD,
        }
        files = {
            'certificate': SimpleUploadedFile('certificate.pdf', b'test', 'application/pdf'),
        }
        form = PortraitForm(data=data, files=files, participant=self.participant)
        self.assertTrue(form.is_valid())


class SeatFormTest(TestCase):
    def setUp(self) -> None:
        user = User.objects.create_user(username='john')
        congress = Congress.objects.create(title="FaTaMa 2024", location="Magdeburg")
        council = Council.objects.create(
            owner=user,
            university="Otto-von-Guericke-Universität Magdeburg",
            name="Fachschaftsrat Maschinenbau",
        )
        attendance = Attendance.objects.create(congress=congress, council=council)
        self.ids = [attendance.pk]

    def test_form(self):
        form = SeatForm(ids=self.ids, data={'seats': 5})
        self.assertTrue(form.is_valid())
