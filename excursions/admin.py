import csv

from django.contrib import admin
from django.http import HttpResponse

from excursions.models import Excursion, Order


@admin.register(Excursion)
class ExcursionAdmin(admin.ModelAdmin):
    list_display = ["title"]
    list_filter = ["congress"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display =["participant", "priority"]
    list_filter = ["excursion"]
    actions = ["export_orders"]

    @admin.action(description="Export selected orders as CSV")
    def export_orders(self, request, queryset) -> HttpResponse:
        response = HttpResponse(
            content_type="text/csv",
            headers={"Content-Disposition": 'attachment; filename="Exkursionen.csv"'},
        )

        writer = csv.writer(response)
        writer.writerow(["Exkursion", "Nachname", "Vorname",  "Priorität"])
        for order in queryset.order_by("excursion__title", "-priority", "participant__last_name", "participant__first_name"):
            writer.writerow([
                order.excursion.title,
                order.participant.last_name,
                order.participant.first_name,
                order.priority,
            ])

        return response
