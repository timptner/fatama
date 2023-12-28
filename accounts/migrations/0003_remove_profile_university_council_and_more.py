# Generated by Django 5.0 on 2023-12-28 22:22

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_profile_options_invite'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='university',
        ),
        migrations.CreateModel(
            name='Council',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('university', models.CharField(max_length=150, verbose_name='Universität')),
                ('name', models.CharField(verbose_name='Name')),
                ('owner', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddConstraint(
            model_name='council',
            constraint=models.UniqueConstraint(fields=('university', 'name'), name='unique_council'),
        ),
    ]
