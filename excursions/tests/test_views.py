from django.test import TestCase
from django.urls import reverse

from accounts.models import Council, User
from congresses.models import Attendance, Congress, Participant
from excursions.models import Excursion


class ExcursionListView(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(username="john")
        self.path = reverse("excursions:excursion_list")

    def test_public_view(self) -> None:
        response = self.client.get(self.path)
        path = reverse("accounts:login")
        self.assertRedirects(response, f"{path}?next={self.path}")

    def test_user_view(self) -> None:
        self.client.force_login(self.user)
        response = self.client.get(self.path)
        self.assertContains(response, "Exkursionen")

    def test_attendant_view(self) -> None:
        user = User.objects.create(username="jane")
        council = Council.objects.create(university="University", name="Student Council", owner=user)
        congress = Congress.objects.create(title="Congress", year=2024)
        attendance = Attendance.objects.create(congress=congress, council=council)
        self.client.force_login(user)
        response = self.client.get(self.path)
        self.assertContains(response, "Exkursionen")
        self.assertContains(response, "Anmeldung")


class CreateOrderViewTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(username="john")
        council = Council.objects.create(owner=self.user)
        self.congress = Congress.objects.create(year=2024)
        attendance = Attendance.objects.create(congress=self.congress, council=council)
        participant = Participant.objects.create(first_name="John", last_name="Doe", attendance=attendance)
        self.path = reverse("congresses:create_order", kwargs={"pk": attendance.pk})

    def test_public_view(self) -> None:
        response = self.client.get(self.path)
        path = reverse("accounts:login")
        self.assertRedirects(response, f"{path}?next={self.path}")

    def test_public_form_view(self) -> None:
        response = self.client.post(self.path)
        path = reverse("accounts:login")
        self.assertRedirects(response, f"{path}?next={self.path}")

    def test_user_view(self) -> None:
        self.client.force_login(self.user)
        response = self.client.get(self.path)
        self.assertContains(response, "Anmeldung zu Exkursionen")

    def test_user_form_view(self) -> None:
        self.client.force_login(self.user)
        excursion1 = Excursion.objects.create(congress=self.congress, title="OVGU")
        excursion2 = Excursion.objects.create(congress=self.congress, title="Intel")
        excursion3 = Excursion.objects.create(congress=self.congress, title="FAM")
        data = {
            "id_form-0-excursion": excursion1,
            "id_form-1-excursion": excursion2,
            "id_form-2-excursion": excursion3,
        }
        response = self.client.post(self.path, data=data)
        self.assertContains(response, "Anmeldung zu Exkursionen")
