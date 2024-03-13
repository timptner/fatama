from django import forms

from fatama.forms import ModelForm
from workshops.models import Workshop


class WorkshopForm(ModelForm):
    class Meta:
        model = Workshop
        fields = ["title", "description"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "input"}),
            "description": forms.Textarea(attrs={"class": "textarea"}),
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def save(self, commit: bool = True):
        workshop = super().save(commit=False)
        workshop.state = Workshop.SUGGESTED
        workshop.author = self.user
        if commit:
            workshop.save()
        return workshop
