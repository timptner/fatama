from django.db import models
from django.db.models import constraints

from congresses.models import Congress, Participant
from fatama.templatetags.markdown import help_text


class Excursion(models.Model):
    congress = models.ForeignKey(Congress, on_delete=models.CASCADE)
    title = models.CharField("Titel", max_length=200)
    url = models.URLField("Webadresse", blank=True)
    desc = models.TextField(
        "Beschreibung",
        help_text=help_text,
    )

    class Meta:
        verbose_name = "Exkursion"
        verbose_name_plural = "Exkursionen"
        ordering = ["title"]
        constraints = [
            models.UniqueConstraint(
                fields=["congress", "title"], name="unique_excursion"
            ),
        ]

    def __str__(self) -> str:
        return str(self.title)


class Order(models.Model):
    excursion = models.ForeignKey(Excursion, on_delete=models.CASCADE)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    priority = models.PositiveSmallIntegerField("Priorität")
    created_at = models.DateTimeField("Erstellt am", auto_now_add=True)

    class Meta:
        verbose_name = "Bestellung"
        verbose_name_plural = "Bestellungen"
        ordering = ["excursion", "participant", "-priority"]
        constraints = [
            models.UniqueConstraint(
                fields=["excursion", "participant"], name="unique_order"
            ),
        ]
