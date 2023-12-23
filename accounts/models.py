from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    university = models.CharField('Universität', max_length=150)

    def __str__(self) -> str:
        return str(self.user)
