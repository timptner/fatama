from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import ListView

from congresses.models import Congress, Participant


class CongressesListView(LoginRequiredMixin, ListView):
    model = Congress


class ParticipantListView(LoginRequiredMixin, ListView):
    model = Participant

    def get_queryset(self):
        congress = get_object_or_404(Congress, pk=self.kwargs.get('congress_id'))
        return Participant.objects.filter(congress=congress, contact=self.request.user)
