from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from congresses.models import Congress


class CongressesListView(LoginRequiredMixin, ListView):
    model = Congress
