from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    university = models.CharField('Universität', max_length=150)

    class Meta:
        permissions = [
            ('can_invite', "Kann weitere Benutzer einladen"),
        ]

    def __str__(self) -> str:
        return str(self.user)


class Invite(models.Model):
    token = models.CharField('Token', unique=True, max_length=20)
    recipient = models.EmailField('Empfänger')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField('Erstellt am', auto_now_add=True)
    expired_at = models.DateTimeField('Abgelaufen am')

    def __str__(self) -> str:
        return self.recipient

    def is_expired(self) -> bool:
        return self.expired_at < timezone.now()
