from django.contrib.auth.models import User, Permission
from django.test import TestCase
from django.urls import reverse

from accounts.models import Council
from congresses.models import Attendance, Congress, Participant, Portrait


class AttendanceCreateViewTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username="john")
        Council.objects.create(
            owner=self.user,
            university="Otto-von-Guericke-Universität Magdeburg",
            name="Fachschaftsrat Maschinenbau",
        )
        self.congress = Congress.objects.create(
            title="Tagung", location="Magdeburg", year=2024
        )
        self.path = reverse(
            "congresses:create_attendance", kwargs={"year": self.congress.year}
        )

    def test_public_view(self):
        response = self.client.get(self.path)
        path = reverse("accounts:login")
        self.assertRedirects(response, f"{path}?next={self.path}")

    def test_public_form_view(self):
        response = self.client.post(self.path)
        path = reverse("accounts:login")
        self.assertRedirects(response, f"{path}?next={self.path}")

    def test_user_view(self):
        self.client.force_login(self.user)
        response = self.client.get(self.path)
        self.assertContains(response, "Zur Tagung anmelden")

    def test_user_form_view(self):
        self.client.force_login(self.user)
        response = self.client.post(self.path)
        self.assertRedirects(
            response,
            reverse("congresses:congress_detail", kwargs={"year": self.congress.year}),
        )


class AttendanceDetailViewTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username="john")
        council = Council.objects.create(
            owner=self.user,
            university="Otto-von-Guericke-Universität Magdeburg",
            name="Fachschaftsrat Maschinenbau",
        )
        congress = Congress.objects.create(
            title="Tagung", location="Magdeburg", year=2024
        )
        self.attendance = Attendance.objects.create(congress=congress, council=council)
        self.path = reverse(
            "congresses:attendance_detail", kwargs={"pk": self.attendance.pk}
        )

    def test_public_view(self):
        response = self.client.get(self.path)
        path = reverse("accounts:login")
        self.assertRedirects(response, f"{path}?next={self.path}")

    def test_user_view(self):
        self.client.force_login(self.user)
        response = self.client.get(self.path)
        self.assertContains(response, "Details zur Teilnahme")


class AttendanceListView(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username="john")
        staff = User.objects.create_user(username="jane")
        staff.is_staff = True
        staff.save()
        self.staff = staff
        council = Council.objects.create(
            owner=self.user,
            university="Otto-von-Guericke-Universität Magdeburg",
            name="Fachschaftsrat Maschinenbau",
        )
        congress = Congress.objects.create(
            title="Tagung", location="Magdeburg", year=2024
        )
        self.attendance = Attendance.objects.create(congress=congress, council=council)
        self.path = reverse("congresses:attendance_list")

    def test_public_view(self) -> None:
        response = self.client.get(self.path)
        path = reverse("accounts:login")
        self.assertRedirects(response, f"{path}?next={self.path}")

    def test_user_view(self) -> None:
        self.client.force_login(self.user)
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 403)

    def test_staff_view(self) -> None:
        self.client.force_login(self.staff)
        response = self.client.get(self.path)
        self.assertContains(response, "Liste aller Besuche")


class CongressDetailViewTest(TestCase):
    def setUp(self) -> None:
        self.congress = Congress.objects.create(
            title="FaTaMa 2024", location="Magdeburg", year=2024
        )
        self.path = reverse(
            "congresses:congress_detail", kwargs={"year": self.congress.year}
        )
        self.user = User.objects.create_user(username="john")

    def test_view(self) -> None:
        response = self.client.get(self.path)
        path = reverse("accounts:login")
        self.assertRedirects(response, f"{path}?next={self.path}")

    def test_user_view(self) -> None:
        self.client.force_login(self.user)
        response = self.client.get(self.path)
        self.assertContains(response, self.congress.title)


class ParticipantCreateViewTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username="john")
        council = Council.objects.create(
            owner=self.user,
            university="Otto-von-Guericke-Universität Magdeburg",
            name="Fachschaftsrat Maschinenbau",
        )
        congress = Congress.objects.create(
            title="Tagung", location="Magdeburg", year=2024
        )
        self.attendance = Attendance.objects.create(congress=congress, council=council)
        self.path = reverse(
            "congresses:create_participant", kwargs={"pk": self.attendance.pk}
        )

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
        self.assertContains(response, "Teilnehmer anmelden")

    def test_user_form_view(self) -> None:
        self.client.force_login(self.user)
        data = {
            "first_name": "John",
            "last_name": "Doe",
        }
        response = self.client.post(self.path, data=data)
        path = reverse(
            "congresses:attendance_detail", kwargs={"pk": self.attendance.pk}
        )
        self.assertRedirects(response, path)


class PortraitCreateViewTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username="john")
        council = Council.objects.create(
            owner=self.user,
            university="Otto-von-Guericke-Universität Magdeburg",
            name="Fachschaftsrat Maschinenbau",
        )
        congress = Congress.objects.create(
            title="Tagung", location="Magdeburg", year=2024
        )
        self.attendance = Attendance.objects.create(congress=congress, council=council)
        self.participant = Participant.objects.create(
            attendance=self.attendance, first_name="John", last_name="Doe"
        )
        self.path = reverse(
            "congresses:create_portrait", kwargs={"pk": self.participant.pk}
        )

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
        self.assertContains(response, "Portrait erstellen")

    def test_user_form_view(self) -> None:
        self.client.force_login(self.user)
        with open("data/certificate.pdf", "rb") as file:
            data = {
                "diet": Portrait.OMNIVORE,
                "intolerance": "Nüsse",
                "size": Portrait.MEDIUM,
                "railcard": Portrait.NO_TICKET,
                "certificate": file,
            }
            response = self.client.post(self.path, data=data)
        path = reverse(
            "congresses:attendance_detail", kwargs={"pk": self.attendance.pk}
        )
        self.assertRedirects(response, path)


class SeatFormViewTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username="john", is_staff=True)
        permission = Permission.objects.get(codename="view_attendance")
        self.user.user_permissions.add(permission)
        congress = Congress.objects.create(
            title="Tagung", location="Magdeburg", year=2024
        )
        council = Council.objects.create(
            owner=self.user,
            university="Otto-von-Guericke-Universität Magdeburg",
            name="Fachschaftsrat Magdeburg",
        )
        attendance = Attendance.objects.create(congress=congress, council=council)
        self.ids = [str(attendance.pk)]
        ids = ",".join(self.ids)
        self.path = reverse("congresses:update_seats") + f"?ids={ids}"

    def test_public_view(self):
        response = self.client.get(self.path)
        path = reverse("accounts:login")
        self.assertRedirects(response, f"{path}?next={self.path}")

    def test_public_form_view(self):
        response = self.client.post(self.path)
        path = reverse("accounts:login")
        self.assertRedirects(response, f"{path}?next={self.path}")

    def test_user_view(self):
        self.client.force_login(self.user)
        response = self.client.get(self.path)
        self.assertContains(response, "Teilnehmerplätze aktualisieren")

    def test_user_form_view(self):
        self.client.force_login(self.user)
        response = self.client.post(self.path, data={"seats": 5})
        self.assertRedirects(
            response, reverse("admin:congresses_attendance_changelist")
        )
