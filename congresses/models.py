from pathlib import Path
from typing import Optional

from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse

from accounts.models import Council


class Congress(models.Model):
    title = models.CharField("Titel", max_length=50, unique=True)
    location = models.CharField("Austragungsort", max_length=150)

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse('congresses:congress-detail', kwargs={'pk': self.pk})

    def get_attendance(self, user: User) -> Optional['Attendance']:
        try:
            attendance = self.attendance_set.filter(council__owner=user).get()
        except Attendance.DoesNotExist:
            attendance = None
        return attendance


class Attendance(models.Model):
    congress = models.ForeignKey(Congress, on_delete=models.CASCADE)
    council = models.ForeignKey(Council, on_delete=models.PROTECT)
    seats = models.PositiveSmallIntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['congress', 'council'], name='unique-attendance')
        ]

    def __str__(self) -> str:
        return f'{self.council} ({self.congress})'

    def get_absolute_url(self):
        return reverse('congresses:attendance-detail', kwargs={'pk': self.pk})

    def remaining_seats(self) -> int:
        return max(self.seats - self.participant_set.count(), 0)


class Participant(models.Model):
    attendance = models.ForeignKey(Attendance, on_delete=models.CASCADE)
    first_name = models.CharField("Vorname", max_length=50)
    last_name = models.CharField("Nachname", max_length=50)

    def __str__(self) -> str:
        return self.full_name

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"


def participant_directory_path(instance, filename) -> str:
    pk = instance.participant.id
    suffix = Path(filename).suffix.lower()
    return f'certificates/participant_{pk:06d}/certificate{suffix}'


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
    STUDENT_CARD = 'CARD'
    INDEPENDENT = 'SELF'
    RAILCARD_CHOICES = {
        NO_TICKET: "Nicht vorhanden",
        STUDENT_CARD: "Im Studentenausweis inbegriffen",
        INDEPENDENT: "Eigenständig erworben",
    }
    participant = models.OneToOneField(Participant, on_delete=models.CASCADE)
    diet = models.CharField("Ernährungsweise", choices=DIET_CHOICES, max_length=2)
    intolerances = models.CharField("Unverträglichkeiten", max_length=200, blank=True)
    railcard = models.CharField("Deutschlandticket", choices=RAILCARD_CHOICES, max_length=4)
    certificate = models.FileField("Immatrikulationsbescheinigung", upload_to=participant_directory_path,
                                   validators=[FileExtensionValidator(['pdf'])], null=True)

    def __str__(self) -> str:
        return str(self.participant)
