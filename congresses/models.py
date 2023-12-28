from django.contrib.auth.models import User
from django.db import models


class Congress(models.Model):
    title = models.CharField("Titel", max_length=50, unique=True)
    location = models.CharField("Austragungsort", max_length=150)

    def __str__(self) -> str:
        return self.title


class Participant(models.Model):
    congress = models.ForeignKey(Congress, on_delete=models.CASCADE)
    first_name = models.CharField("Vorname", max_length=50)
    last_name = models.CharField("Nachname", max_length=50)
    contact = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return self.full_name

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Portrait(models.Model):
    VEGAN = 'V+'
    VEGETARIAN = 'V'
    OMNIVORE = 'O'
    DIET_CHOICES = {
        VEGAN: 'Vegan',
        VEGETARIAN: 'Vegetarisch',
        OMNIVORE: 'Omnivore',
    }
    NO_TICKET = 'NONE'
    BAHNCARD_25 = '25'
    BAHNCARD_50 = '50'
    BAHNCARD_100 = '100'
    GERMANY_TICKET = 'FREE'
    RAILCARD_CHOICES = {
        NO_TICKET: 'Keine Vergünstigung',
        BAHNCARD_25: 'BahnCard 25',
        BAHNCARD_50: 'BahnCard 50',
        BAHNCARD_100: 'BahnCard 100',
        GERMANY_TICKET: 'Deutschlandticket',
    }
    participant = models.OneToOneField(Participant, on_delete=models.CASCADE)
    diet = models.CharField("Ernährungsweise", choices=DIET_CHOICES, max_length=2)
    intolerances = models.CharField("Unverträglichkeiten", max_length=200, blank=True)
    railcard = models.CharField("Bahn-Ticket", choices=RAILCARD_CHOICES, max_length=4)

    def __str__(self) -> str:
        return str(self.participant)
