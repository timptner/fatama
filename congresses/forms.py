from django import forms
from django.core.mail import send_mail, send_mass_mail
from django.urls import reverse_lazy

from congresses.models import Attendance, Participant, Portrait


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = []

    def __init__(self, congress, council, *args, **kwargs) -> None:
        self.congress = congress
        self.council = council
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        attendance = super().save(commit=False)
        attendance.congress = self.congress
        attendance.council = self.council
        if commit:
            attendance.save()
        return attendance


class AttendanceAdminForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['congress', 'council', 'seats']

    def __init__(self, *args, **kwargs):
        self.request = None
        super().__init__(*args, **kwargs)

    def send_mail(self, request) -> None:
        subject, message, sender, recipients = get_seat_update_mail(self.instance, request)
        send_mail(subject, message, sender, recipients)


class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['first_name', 'last_name']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'input'}),
            'last_name': forms.TextInput(attrs={'class': 'input'}),
        }

    def __init__(self, attendance, *args, **kwargs):
        self.attendance = attendance
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        participant = super().save(commit=False)
        participant.attendance = self.attendance
        if commit:
            participant.save()
        return participant


class PortraitForm(forms.ModelForm):
    class Meta:
        model = Portrait
        fields = ['diet', 'intolerances', 'railcard']
        widgets = {
            'intolerances': forms.TextInput(attrs={'class': 'input'}),
        }
        help_texts = {
            'intolerances': "Optional.",
        }

    def __init__(self, participant, *args, **kwargs) -> None:
        self.participant = participant
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        portrait = super().save(commit=False)
        portrait.participant = self.participant
        if commit:
            portrait.save()
        return portrait


def get_seat_update_mail(attendance: Attendance, request):
    scheme = 'https' if request.is_secure() else 'http'
    host = request.get_host()
    path = reverse_lazy('congresses:attendance-detail', kwargs={'pk': attendance.pk})
    user = attendance.council.owner
    subject = "Teilnehmerplätze aktualisiert"
    message = f"""Hallo {user.first_name},

die Teilnehmerplätze für die Anmeldung deines Gremiums {attendance.council} zur Tagung {attendance.congress} wurden aktualisiert.

{scheme}://{host}{path}"""
    sender = None
    recipients = [user.email]

    return (
        subject,
        message,
        sender,
        recipients,
    )


class SeatForm(forms.Form):
    seats = forms.IntegerField(
        label="Plätze",
        widget=forms.NumberInput(attrs={'class': 'input'}),
    )

    def __init__(self, ids, *args, **kwargs):
        self.ids = ids
        super().__init__(*args, **kwargs)

    def save(self, request) -> int:
        seats = self.cleaned_data.get('seats')
        queryset = Attendance.objects.filter(pk__in=self.ids)
        updated = queryset.update(seats=seats)
        mails = [get_seat_update_mail(attendance, request) for attendance in queryset]
        send_mass_mail(mails)
        return updated
