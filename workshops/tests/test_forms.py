from django.contrib.auth.models import User
from django.test import TestCase

from workshops.forms import WorkshopForm


class WorkshopFormTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username="john")

    def test_form(self) -> None:
        data = {
            "title": "Foo",
            "description": "Bar",
        }
        form = WorkshopForm(data=data, user=self.user)
        self.assertTrue(form.is_valid())
