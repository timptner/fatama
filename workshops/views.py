from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from congresses.models import Congress
from workshops.forms import WorkshopForm
from workshops.models import Workshop


class WorkshopCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = WorkshopForm
    template_name = "workshops/workshop_form.html"
    success_url = reverse_lazy("workshops:workshop_list")
    success_message = "Seminar wurde erstellt."

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        congress = Congress.objects.order_by("-year").first()
        kwargs.update({"user": self.request.user, "congress": congress})
        return kwargs


class WorkshopListView(LoginRequiredMixin, ListView):
    model = Workshop
