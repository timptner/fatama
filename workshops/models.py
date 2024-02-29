from django.db import models

from accounts.models import User


class Workshop(models.Model):
    SUGGESTED = 'S'
    APPROVED = 'A'
    REJECTED = 'R'
    STATE_CHOICES = {
        SUGGESTED: "Vorgeschlagen",
        APPROVED: "Angenommen",
        REJECTED: "Abgelehnt",
    }
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField("Titel", max_length=200, unique=True)
    description = models.TextField("Beschreibung")
    state = models.CharField("Status", max_length=1, choices=STATE_CHOICES)

    class Meta:
        verbose_name = "Seminar"
        verbose_name_plural = "Seminare"
        ordering = ['title']

    def __str__(self) -> str:
        return self.title
