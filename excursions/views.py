from django.db.models import Count, Q
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from congresses.models import Congress
from excursions.models import Excursion


class ExcursionListView(LoginRequiredMixin, ListView):
    model = Excursion

    def get_queryset(self):
        congress = Congress.objects.order_by("-year").first()
        queryset = (
            Excursion.objects.filter(congress=congress)
                .annotate(prio1=Count("order", filter=Q(order__priority=1)))
                .annotate(prio2=Count("order", filter=Q(order__priority=2)))
                .annotate(prio3=Count("order", filter=Q(order__priority=3)))
        )
        return queryset
