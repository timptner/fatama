from django import forms

from congresses.models import Participant


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
