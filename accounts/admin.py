from django.contrib import admin

from accounts.models import Council, Profile, Invite


@admin.register(Council)
class CouncilAdmin(admin.ModelAdmin):
    list_display = ["name", "university", "owner"]
    list_filter = ["university"]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(Invite)
class InviteAdmin(admin.ModelAdmin):
    readonly_fields = ["token"]
    list_display = ["recipient", "sender", "is_active"]
    list_filter = ["sender"]
    date_hierarchy = "expired_at"

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
