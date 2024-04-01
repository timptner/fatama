from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from congresses.models import Attendance, Congress, Participant
from excursions.forms import OrderFormSet
from excursions.models import Excursion, Order


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

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        try:
            attendance = Attendance.objects.get(council__owner=self.request.user)
        except Attendance.DoesNotExist:
            attendance = None
        context["attendance"] = attendance
        return context


@login_required
def create_order(request, pk):
    participant = get_object_or_404(Participant, pk=pk)
    if participant.attendance.council.owner != request.user:
        raise PermissionDenied()

    if request.method == "POST":
        formset = OrderFormSet(request.POST, form_kwargs={"participant": participant})
        if formset.is_valid():
            for form in formset:
                form.save()
            messages.success(request, f"Exkursion für <strong>{participant}</strong> erstellt.")
            return redirect("congresses:attendance_detail", pk=participant.attendance.pk)
    else:
        formset = OrderFormSet(form_kwargs={"participant": participant})

    context = {
        "participant": participant,
        "formset": formset,
    }
    return render(request, "excursions/order_form.html", context)
