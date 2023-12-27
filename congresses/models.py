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
        return f"{self.first_name} {self.last_name}"
