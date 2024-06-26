from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Council(models.Model):
    owner = models.OneToOneField(User, on_delete=models.PROTECT)
    university = models.CharField(
        "Universität", max_length=150, help_text="Vermeide Akronyme."
    )
    name = models.CharField("Name", help_text="Name deiner Fachschaft.")

    class Meta:
        verbose_name = "Gremium"
        verbose_name_plural = "Gremien"
        ordering = ["university", "name"]
        constraints = [
            models.UniqueConstraint(
                fields=["university", "name"], name="unique_council"
            ),
        ]

    def __str__(self) -> str:
        return f"{self.name} ({self.university})"

    def get_years(self) -> list[int]:
        return self.attendance_set.values_list("congress__year", flat=True)


class Invite(models.Model):
    token = models.CharField("Token", unique=True, max_length=20)
    recipient = models.EmailField("Empfänger")
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField("Erstellt am", auto_now_add=True)
    expired_at = models.DateTimeField("Abgelaufen am")

    class Meta:
        verbose_name = "Einladung"
        verbose_name_plural = "Einladungen"
        ordering = ["recipient"]

    def __str__(self) -> str:
        return self.recipient

    def is_expired(self) -> bool:
        return self.expired_at < timezone.now()

    is_expired.boolean = True
    is_expired.short_description = "Expired"

    def is_active(self) -> bool:
        return not self.is_expired()

    is_active.boolean = True
    is_active.short_description = "Active"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Profil"
        verbose_name_plural = "Profile"
        permissions = [
            ("can_invite", "Kann weitere Benutzer einladen"),
        ]

    def __str__(self) -> str:
        return str(self.user)
