from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from congresses.forms import ParticipantForm
from congresses.models import Congress, Participant


class CongressesListView(LoginRequiredMixin, ListView):
    model = Congress


class ParticipantCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = ParticipantForm
    success_message = "Teilnehmer erfolgreich hinzugefügt"
    template_name = 'congresses/participant_form.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['congress'] = get_object_or_404(Congress, pk=self.kwargs.get('congress_id'))
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['congress'] = get_object_or_404(Congress, pk=self.kwargs.get('congress_id'))
        return kwargs

    def get_success_url(self):
        congress = get_object_or_404(Congress, pk=self.kwargs.get('congress_id'))
        return reverse_lazy('congresses:participant_list', kwargs={'congress_id': congress.pk})


class ParticipantListView(LoginRequiredMixin, ListView):
    model = Participant

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['congress'] = get_object_or_404(Congress, pk=self.kwargs.get('congress_id'))
        return context

    def get_queryset(self):
        congress = get_object_or_404(Congress, pk=self.kwargs.get('congress_id'))
        return Participant.objects.filter(congress=congress, contact=self.request.user)
