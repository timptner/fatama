from django.views.generic import CreateView, ListView

from .models import Workshop


class WorkshopCreateView(CreateView):
    model = Workshop


class WorkshopListView(ListView):
    model = Workshop
