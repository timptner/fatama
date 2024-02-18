from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, FormView, ListView

from congresses.forms import AttendanceForm, ParticipantForm, PortraitForm, SeatForm
from congresses.models import Attendance, Congress, Participant


class AttendanceCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = AttendanceForm
    success_message = "Dein Gremium wurde für die Tagung angemeldet."
    template_name = 'congresses/attendance_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['congress'] = get_object_or_404(Congress, year=self.kwargs['year'])
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['congress'] = get_object_or_404(Congress, year=self.kwargs['year'])
        kwargs['council'] = self.request.user.council
        return kwargs

    def get_success_url(self):
        return reverse_lazy('congresses:congress_detail', kwargs={'year': self.kwargs['year']})


class AttendanceDetailsView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Attendance

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['congress'] = self.object.congress
        return context

    def test_func(self) -> bool:
        user = self.request.user
        attendance = get_object_or_404(Attendance, pk=self.kwargs['pk'])
        if user.is_superuser:
            return True
        elif attendance.council.owner == user:
            return True
        else:
            return False


class CongressDetailView(LoginRequiredMixin, DetailView):
    model = Congress

    def get_object(self, queryset=None):
        return get_object_or_404(Congress, year=self.kwargs['year'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['attendance'] = self.object.get_attendance(self.request.user)
        return context


class CongressListView(LoginRequiredMixin, ListView):
    model = Congress


class ParticipantCreateView(LoginRequiredMixin, SuccessMessageMixin, UserPassesTestMixin, CreateView):
    form_class = ParticipantForm
    success_message = "Teilnehmer wurde hinzugefügt."
    template_name = 'congresses/participant_form.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        attendance = get_object_or_404(Attendance, pk=self.kwargs['pk'])
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['attendance'] = attendance
        context['congress'] = attendance.congress
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['attendance'] = get_object_or_404(Attendance, pk=self.kwargs['pk'])
        return kwargs

    def get_success_url(self):
        return reverse_lazy('congresses:attendance_detail', kwargs={'pk': self.kwargs['pk']})

    def test_func(self) -> bool:
        user = self.request.user
        attendance = get_object_or_404(Attendance, pk=self.kwargs['pk'])
        if user.is_superuser:
            return True
        elif attendance.council.owner == user:
            return True
        else:
            return False


class PortraitCreateView(LoginRequiredMixin, SuccessMessageMixin, UserPassesTestMixin, CreateView):
    form_class = PortraitForm
    success_message = "Portrait wurde erstellt."
    template_name = 'congresses/portrait_form.html'

    def get_context_data(self, **kwargs):
        participant = get_object_or_404(Participant, pk=self.kwargs['pk'])
        context = super().get_context_data(**kwargs)
        context['participant'] = participant
        context['attendance'] = participant.attendance
        context['congress'] = participant.attendance.congress
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['participant'] = get_object_or_404(Participant, pk=self.kwargs['pk'])
        return kwargs

    def get_success_url(self):
        participant = get_object_or_404(Participant, pk=self.kwargs['pk'])
        return reverse_lazy('congresses:attendance_detail', kwargs={'pk': participant.attendance.pk})

    def test_func(self) -> bool:
        user = self.request.user
        participant = get_object_or_404(Participant, pk=self.kwargs['pk'])
        if user.is_superuser:
            return True
        elif participant.attendance.council.owner == user:
            return True
        else:
            return False


class SeatFormView(LoginRequiredMixin, SuccessMessageMixin, UserPassesTestMixin, FormView):
    form_class = SeatForm
    template_name = 'congresses/update_seats.html'
    success_message = "Attendances were successfully updated."
    success_url = reverse_lazy('admin:congresses_attendance_changelist')

    def form_valid(self, form):
        form.save(self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ids = self.request.GET.get('ids')
        if ids:
            ids = ids.split(',')
        else:
            ids = []
        context = super().get_context_data(**kwargs)
        context['attendance_list'] = Attendance.objects.filter(pk__in=ids)
        return context

    def get_form_kwargs(self):
        ids = self.request.GET.get('ids')
        if ids:
            ids = ids.split(',')
        else:
            ids = []
        kwargs = super().get_form_kwargs()
        kwargs['ids'] = ids
        return kwargs

    def test_func(self) -> bool:
        user = self.request.user
        if user.is_superuser:
            return True
        elif user.is_staff:
            return True
        else:
            return False
