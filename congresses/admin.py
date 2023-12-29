from django.contrib import admin

from congresses.models import Attendance, Congress, Participant, Portrait


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    pass


@admin.register(Congress)
class CongressAdmin(admin.ModelAdmin):
    pass


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_filter = ['attendance']


@admin.register(Portrait)
class PortraitAdmin(admin.ModelAdmin):
    pass
