# Generated by Django 5.0.3 on 2024-03-13 22:20

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("congresses", "0009_congress_support_email_congress_support_team"),
        ("workshops", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="workshop",
            name="comment",
            field=models.TextField(blank=True, verbose_name="Kommentar"),
        ),
        migrations.AddField(
            model_name="workshop",
            name="congress",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="congresses.congress",
            ),
        ),
        migrations.AddConstraint(
            model_name="workshop",
            constraint=models.CheckConstraint(
                check=models.Q(
                    ("state", "S"),
                    models.Q(("state", "R"), models.Q(("comment", ""), _negated=True)),
                    ("state", "A"),
                    _connector="OR",
                ),
                name="comment_when_rejected",
                violation_error_message="Bei Ablehnung ist eine Begründung anzugeben.",
            ),
        ),
    ]
