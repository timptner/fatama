from django.test import TestCase

from accounts.models import Council, User
from congresses.models import Attendance, Congress, Participant
from excursions.forms import OrderForm, OrderFormSet
from excursions.models import Excursion


class OrderFormTest(TestCase):
    def setUp(self) -> None:
        user = User.objects.create(username="john")
        council = Council.objects.create(university="University", name="Student Council", owner=user)
        congress = Congress.objects.create(year=2024)
        self.excursion = Excursion.objects.create(congress=congress, title="OVGU")
        attendance = Attendance.objects.create(congress=congress, council=council)
        self.participant = Participant.objects.create(first_name="John", last_name="Doe", attendance=attendance)

    def test_form(self) -> None:
        data = {
            "excursion": self.excursion,
        }
        form = OrderForm(data=data, participant=self.participant, priority=1)
        self.assertTrue(form.is_valid())


class OrderFormSetTest(TestCase):
    def setUp(self) -> None:
        user = User.objects.create(username="john")
        council = Council.objects.create(university="University", name="Student Council", owner=user)
        self.congress = Congress.objects.create(year=2024)
        attendance = Attendance.objects.create(congress=self.congress, council=council)
        self.participant = Participant.objects.create(first_name="John", last_name="Doe", attendance=attendance)

    def test_formset(self) -> None:
        excursion1 = Excursion.objects.create(congress=self.congress, title="OVGU")
        excursion2 = Excursion.objects.create(congress=self.congress, title="Intel")
        excursion3 = Excursion.objects.create(congress=self.congress, title="FAM")
        data = {
            "id_form-0-excursion": excursion1,
            "id_form-1-excursion": excursion2,
            "id_form-2-excursion": excursion3,
        }
        formset = OrderFormSet(data=data, form_kwargs={"participant": self.participant})
