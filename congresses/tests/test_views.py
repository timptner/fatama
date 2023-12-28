from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from congresses.models import Congress


class CongressListView(TestCase):
    def setUp(self) -> None:
        self.path = reverse('congresses:congress_list')
        self.user = User.objects.create_user(username='john')

    def test_view(self) -> None:
        response = self.client.get(self.path)
        path = reverse('accounts:login')
        self.assertRedirects(response, f'{path}?next={self.path}')

    def test_user_view(self) -> None:
        self.client.force_login(self.user)
        response = self.client.get(self.path)
        self.assertContains(response, "Tagungen")


class ParticipantListView(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username='john')
        self.congress = Congress.objects.create(title="FaTaMa 2024", location="Magdeburg")
        self.path = reverse('congresses:participant_list', kwargs={'congress_id': self.congress.pk})

    def test_view(self) -> None:
        response = self.client.get(self.path)
        path = reverse('accounts:login')
        self.assertRedirects(response, f'{path}?next={self.path}')

    def test_user_view(self) -> None:
        self.client.force_login(self.user)
        response = self.client.get(self.path)
        self.assertContains(response, "Teilnehmer")


class ParticipantFormView(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username='john')
        self.congress = Congress.objects.create(title="FaTaMa 2024", location="Magdeburg")
        self.path = reverse('congresses:create_participant', kwargs={'congress_id': self.congress.pk})

    def test_view(self) -> None:
        response = self.client.get(self.path)
        path = reverse('accounts:login')
        self.assertRedirects(response, f'{path}?next={self.path}')

    def test_post_view(self) -> None:
        response = self.client.post(self.path)
        path = reverse('accounts:login')
        self.assertRedirects(response, f'{path}?next={self.path}')

    def test_user_view(self) -> None:
        self.client.force_login(self.user)
        response = self.client.get(self.path)
        self.assertContains(response, "Teilnehmer ergänzen")

    def test_user_post_view(self) -> None:
        self.client.force_login(self.user)
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
        }
        response = self.client.post(self.path, data=data)
        path = reverse('congresses:participant_list', kwargs={'congress_id': self.congress.pk})
        self.assertRedirects(response, path)

