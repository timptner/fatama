# Generated by Django 5.0 on 2023-12-28 23:48

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


def forwards_func(apps, schema_editor):
    db_alias = schema_editor.connection.alias

    Attendance = apps.get_model("congresses", "Attendance")
    Council = apps.get_model("accounts", "Council")
    Participant = apps.get_model("congresses", "Participant")

    contacts = (
        Participant.objects.using(db_alias).distinct().values_list("contact", flat=True)
    )
    Council.objects.using(db_alias).bulk_create(
        [
            Council(
                owner_id=contact, university="Universität", name=f"Gremium {contact}"
            )
            for contact in contacts
            if not Council.objects.using(db_alias).filter(owner_id=contact).exists()
        ]
    )

    Attendance.objects.using(db_alias).bulk_create(
        [
            Attendance(
                council=Council.objects.using(db_alias).get(owner_id=contact),
                congress_id=congress,
            )
            for congress, contact in Participant.objects.using(db_alias)
            .distinct()
            .values_list("congress", "contact")
        ]
    )

    participants = Participant.objects.using(db_alias).all()
    for participant in participants:
        participant.attendance = Attendance.objects.using(db_alias).get(
            council__owner_id=participant.contact,
            congress_id=participant.congress,
        )
    Participant.objects.using(db_alias).bulk_update(participants, ["attendance"])


def reverse_func(apps, schema_editor):
    db_alias = schema_editor.connection.alias
    Participant = apps.get_model("congresses", "Participant")
    participants = (
        Participant.objects.using(db_alias).select_related("attendance").all()
    )
    for participant in participants:
        participant.contact = participant.attendance.council.owner
        participant.congress = participant.attendance.congress
    Participant.objects.using(db_alias).bulk_update(
        participants, ["congress", "contact"]
    )


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0003_remove_profile_university_council_and_more"),
        ("congresses", "0002_portrait"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Attendance",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("seats", models.PositiveSmallIntegerField(default=0)),
                (
                    "congress",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="congresses.congress",
                    ),
                ),
                (
                    "council",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="accounts.council",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="participant",
            name="attendance",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="congresses.attendance",
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="participant",
            name="congress",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="congresses.congress",
                null=True,
            ),
        ),
        migrations.RunPython(forwards_func, reverse_func),
        migrations.AlterField(
            model_name="participant",
            name="attendance",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="congresses.attendance"
            ),
        ),
        migrations.RemoveField(
            model_name="participant",
            name="congress",
        ),
        migrations.RemoveField(
            model_name="participant",
            name="contact",
        ),
    ]
