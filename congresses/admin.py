from django.contrib import admin

from congresses.models import Congress


@admin.register(Congress)
class CongressAdmin(admin.ModelAdmin):
    pass
