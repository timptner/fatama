from django.contrib import admin, messages
from django.shortcuts import redirect
from django.urls import reverse_lazy

from congresses.models import Attendance, Congress, Participant, Portrait


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['council', 'congress', 'seats']
    list_filter = ['council', 'congress']
    actions = ['add_seats']

    @admin.action(description="Update seats of selected attendances")
    def add_seats(self, request, queryset):
        selected = queryset.values_list('pk', flat=True)
        path = reverse_lazy('congresses:update-seats')
        ids = ','.join([str(pk) for pk in selected])
        return redirect(f'{path}?ids={ids}')


@admin.register(Congress)
class CongressAdmin(admin.ModelAdmin):
    pass


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_filter = ['attendance']


@admin.register(Portrait)
class PortraitAdmin(admin.ModelAdmin):
    pass
