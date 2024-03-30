from django.test import TestCase
from django.urls import reverse

from accounts.models import User


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
