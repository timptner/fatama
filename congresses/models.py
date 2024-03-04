from pathlib import Path
from typing import Optional

from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models import Q
from django.urls import reverse

from accounts.models import Council


class Congress(models.Model):
    year = models.IntegerField("Jahr", unique=True, null=True)
    location = models.CharField("Austragungsort", max_length=150,
                                help_text="Die Stadt reicht aus.")
    title = models.CharField("Titel", max_length=50,
                             help_text="Verwende einen knackigen Titel und nicht nur \"FaTaMa\".")
    message = models.TextField("Botschaft", blank=True)
    support_email = models.EmailField("E-Mail-Adresse", help_text="Erreichbarkeit der Organisatoren.")
    support_team = models.CharField("Team", help_text="Namen der Organisatoren. (Verwendung als Signatur in E-Mails.)")

    class Meta:
        verbose_name = "Tagung"
        verbose_name_plural = "Tagungen"
        ordering = ['-year']
        constraints = [
            models.CheckConstraint(
                check=Q(year__gte=2000) & Q(year__lte=2050),
                name='valid_year',
                violation_error_message="Jahr muss zwischen 2000 und 2050 liegen.",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.title} ({self.year})"

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
        verbose_name = "Besuch"
        verbose_name_plural = "Besuche"
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

    class Meta:
        verbose_name = "Teilnehmer"
        verbose_name_plural = "Teilnehmer"
        ordering = ['first_name', 'last_name']

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
    EXTRA_SMALL = 'XS'
    SMALL = 'S'
    MEDIUM = 'M'
    LARGE = 'L'
    EXTRA_LARGE = 'XL'
    SIZE_CHOICES = {
        EXTRA_SMALL: "Sehr klein (XS)",
        SMALL: "Klein (S)",
        MEDIUM: "Mittel (M)",
        LARGE: "Groß (L)",
        EXTRA_LARGE: "Sehr groß (XL)",
    }
    participant = models.OneToOneField(Participant, on_delete=models.CASCADE)
    diet = models.CharField("Ernährungsweise", choices=DIET_CHOICES, max_length=2)
    intolerances = models.CharField("Unverträglichkeiten", max_length=200, blank=True)
    railcard = models.CharField("Deutschlandticket", choices=RAILCARD_CHOICES, max_length=4)
    certificate = models.FileField("Immatrikulationsbescheinigung", upload_to=participant_directory_path,
                                   validators=[FileExtensionValidator(['pdf'])], null=True)
    size = models.CharField("Konfektionsgröße", choices=SIZE_CHOICES, max_length=2)

    class Meta:
        verbose_name = "Porträt"
        verbose_name_plural = "Porträts"

    def __str__(self) -> str:
        return str(self.participant)
