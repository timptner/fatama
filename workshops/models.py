from django.db import models
from django.db.models import CheckConstraint, Q

from accounts.models import User
from congresses.models import Congress
from fatama.templatetags.markdown import help_text


class Workshop(models.Model):
    SUGGESTED = "S"
    APPROVED = "A"
    REJECTED = "R"
    STATE_CHOICES = {
        SUGGESTED: "Vorgeschlagen",
        APPROVED: "Angenommen",
        REJECTED: "Abgelehnt",
    }
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    is_leader = models.BooleanField(
        "Redeleitung",
        default=True,
        help_text="Die Redeleitung für diesen Workshop übernehmen.",
    )
    title = models.CharField("Titel", max_length=200, unique=True)
    description = models.TextField("Beschreibung", help_text=help_text)
    state = models.CharField("Status", max_length=1, choices=STATE_CHOICES)
    comment = models.TextField("Kommentar", blank=True)
    congress = models.ForeignKey(
        Congress, on_delete=models.SET_NULL, blank=True, null=True
    )

    class Meta:
        verbose_name = "Seminar"
        verbose_name_plural = "Seminare"
        ordering = ["title"]
        constraints = [
            CheckConstraint(
                check=Q(state="S") | (Q(state="R") & ~Q(comment="")) | Q(state="A"),
                name="comment_when_rejected",
                violation_error_message="Bei Ablehnung ist eine Begründung anzugeben.",
            ),
        ]

    def __str__(self) -> str:
        return self.title

    def get_state_color(self) -> str:
        colors = {
            Workshop.SUGGESTED: "is-info",
            Workshop.APPROVED: "is-success",
            Workshop.REJECTED: "is-danger",
        }
        return colors[self.state]
