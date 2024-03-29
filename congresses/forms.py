from django import forms
from django.core.exceptions import ValidationError
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.urls import reverse_lazy

from accounts.models import Council
from congresses.models import Attendance, Congress, Participant, Portrait
from fatama.forms import Form, ModelForm, Select, FileInput
from fatama.postmark import Mail


class AttendanceForm(ModelForm):
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


class AttendanceAdminForm(ModelForm):
    class Meta:
        model = Attendance
        fields = ["congress", "council", "seats"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_seats(self) -> int:
        data = self.cleaned_data["seats"]
        attendance: Attendance = self.instance
        if attendance.pk is not None:
            used = attendance.participant_set.count()
            if data < used:
                raise ValidationError(
                    "Die Anzahl der Plätze kann nicht kleiner als die Anzahl "
                    "bereits angemeldeter Teilnehmer (%(amount)s) sein.",
                    params={"amount": used},
                    code="too_less",
                )
        return data

    def send_mail(self, request) -> None:
        if "seats" in self.changed_data:
            send_seat_update_mail(self.instance, request)


class ExportForm(Form):
    congress = forms.ModelChoiceField(
        queryset=Congress.objects.all(), widget=Select(), label="Tagung"
    )
    council = forms.ModelChoiceField(
        queryset=Council.objects.all(),
        widget=Select(),
        required=False,
        label="Gremium",
        help_text="Optional. Wird keine Auswahl getroffen schließt das alle Gremien im Export ein.",
    )

    def clean(self):
        cleaned_data = super().clean()

        congress = cleaned_data.get("congress")
        council = cleaned_data.get("council")

        if congress and council:
            is_attendant = Attendance.objects.filter(
                congress=congress, council=council
            ).exists()
            if not is_attendant:
                raise ValidationError(
                    "<strong>%(council)s</strong> hat an der Tagung <strong>%(congress)s</strong> nicht teilgenommen.",
                    params={
                        "council": council,
                        "congress": congress,
                    },
                    code="invalid",
                )


class ParticipantForm(ModelForm):
    class Meta:
        model = Participant
        fields = ["first_name", "last_name"]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "input"}),
            "last_name": forms.TextInput(attrs={"class": "input"}),
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


def get_human_size(size: float) -> str:
    """Convert file size (in bytes) to human version."""
    if size > 1e9:
        size = size * 1e-9
        unit = "GB"
    elif size > 1e6:
        size = size * 1e-6
        unit = "MB"
    elif size > 1e3:
        size = size * 1e-3
        unit = "KB"
    else:
        unit = "B"
    return f"{size:.1f} {unit}"


class PortraitForm(ModelForm):
    class Meta:
        model = Portrait
        fields = ["diet", "intolerances", "size", "railcard", "certificate"]
        widgets = {
            "diet": Select(),
            "intolerances": forms.TextInput(attrs={"class": "input"}),
            "size": Select(),
            "railcard": Select(),
            "certificate": FileInput(attrs={"accept": ".pdf"}),
        }
        help_texts = {
            "intolerances": "Optional.",
            "size": "Unisex T-Shirt.",
            "certificate": "PDF-Datei. Maximal 2 MB.",
        }

    def __init__(self, participant, *args, **kwargs) -> None:
        self.participant = participant
        super().__init__(*args, **kwargs)

    def clean_certificate(self):
        certificate = self.cleaned_data.get("certificate")
        if certificate.size > 2e6:
            human_size = get_human_size(certificate.size)
            raise ValidationError(
                "Datei ist zu groß. (%(human_size)s)",
                params={"human_size": human_size},
                code="size_exceeded",
            )
        return certificate

    def save(self, commit=True):
        portrait = super().save(commit=False)
        portrait.participant = self.participant
        if commit:
            portrait.save()
        return portrait


def send_seat_update_mail(attendance: Attendance, request: HttpRequest):
    scheme = "https" if request.is_secure() else "http"
    host = request.get_host()
    path = reverse_lazy("congresses:attendance_detail", kwargs={"pk": attendance.pk})
    user = attendance.council.owner
    url = f"{scheme}://{host}{path}"

    context = {
        "recipient": user.first_name,
        "attendance": attendance,
        "action_url": url,
        "seats": {
            "total": attendance.seats,
            "free": attendance.remaining_seats(),
        },
    }

    mail = Mail(
        "seat-update",
        "Teilnehmerplätze aktualisiert",
        render_to_string("congresses/mails/seat_update.md", context, request),
        user.email,
        stream="broadcast",
    )
    mail.send()


class SeatForm(Form):
    seats = forms.IntegerField(
        label="Plätze",
        widget=forms.NumberInput(attrs={"class": "input"}),
    )

    def __init__(self, ids, *args, **kwargs):
        self.ids = ids
        super().__init__(*args, **kwargs)

    def clean_seats(self) -> int:
        data = self.cleaned_data["seats"]
        queryset = Attendance.objects.filter(pk__in=self.ids)
        for attendance in queryset:
            used = attendance.participant_set.count()
            if data < used:
                error = ValidationError(
                    "%(attendance)s hat bereits %(amount)s Platz belegt."
                    if used == 1
                    else "%(attendance)s hat bereits %(amount)s Plätze belegt.",
                    params={"attendance": attendance, "amount": used},
                    code="too_less",
                )
                self.add_error("seats", error)
        return data

    def save(self, request) -> None:
        seats = self.cleaned_data.get("seats")
        queryset = Attendance.objects.filter(pk__in=self.ids)
        for attendance in queryset:
            if attendance.seats != seats:
                attendance.seats = seats
                attendance.save()
                send_seat_update_mail(attendance, request)
