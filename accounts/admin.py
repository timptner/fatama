from django.contrib import admin

from accounts.models import Council, Profile, Invite


@admin.register(Council)
class CouncilAdmin(admin.ModelAdmin):
    list_display = ['name', 'university', 'owner']
    list_filter = ['university']


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(Invite)
class InviteAdmin(admin.ModelAdmin):
    pass
