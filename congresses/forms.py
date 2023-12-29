from django import forms

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
