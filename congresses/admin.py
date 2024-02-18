from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse_lazy

from congresses.forms import AttendanceAdminForm
from congresses.models import Attendance, Congress, Participant, Portrait


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['council', 'congress', 'seats']
    list_filter = ['council', 'congress__year']
    actions = ['add_seats']
    form = AttendanceAdminForm

    def save_form(self, request, form, change):
        form.send_mail(request)
        return super().save_form(request, form, change)

    @admin.action(description="Update seats of selected attendances")
    def add_seats(self, request, queryset):
        selected = queryset.values_list('pk', flat=True)
        path = reverse_lazy('congresses:update_seats')
        ids = ','.join([str(pk) for pk in selected])
        return redirect(f'{path}?ids={ids}')


@admin.register(Congress)
class CongressAdmin(admin.ModelAdmin):
    list_display = ['title', 'location', 'year']


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_filter = ['attendance']
    list_display = ['full_name', 'attendance']


@admin.register(Portrait)
class PortraitAdmin(admin.ModelAdmin):
    pass
