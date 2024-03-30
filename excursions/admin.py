from django.contrib import admin

from excursions.models import Excursion, Order


@admin.register(Excursion)
class ExcursionAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass
