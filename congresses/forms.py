from django import forms

from congresses.models import Participant, Portrait


class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['first_name', 'last_name']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'input'}),
            'last_name': forms.TextInput(attrs={'class': 'input'}),
        }

    def __init__(self, congress, user, *args, **kwargs):
        self.congress = congress
        self.user = user
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        participant = super().save(commit=False)
        participant.congress = self.congress
        participant.contact = self.user
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
