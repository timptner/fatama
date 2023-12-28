from django.contrib import admin

from congresses.models import Congress, Participant


@admin.register(Congress)
class CongressAdmin(admin.ModelAdmin):
    pass


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_filter = ['congress', 'contact']
