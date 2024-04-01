from django.contrib import admin

from excursions.models import Excursion, Order


@admin.register(Excursion)
class ExcursionAdmin(admin.ModelAdmin):
    list_display = ["title"]
    list_filter = ["congress"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display =["participant", "priority"]
    list_filter = ["excursion"]
