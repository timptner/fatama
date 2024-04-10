from django import forms

from fatama.forms import ModelForm, CheckboxInput
from workshops.models import Workshop


class WorkshopForm(ModelForm):
    class Meta:
        model = Workshop
        fields = ["title", "description", "is_leader"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "input"}),
            "description": forms.Textarea(attrs={"class": "textarea"}),
            "is_leader": CheckboxInput(
                attrs={
                    "label": "Ich werde die Redeleitung für diesen Workshop übernehmen."
                }
            ),
        }
        help_texts = {
            "is_leader": None,
        }

    def __init__(self, user, congress, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.congress = congress

    def save(self, commit: bool = True):
        workshop = super().save(commit=False)
        workshop.state = Workshop.SUGGESTED
        workshop.author = self.user
        workshop.congress = self.congress
        if commit:
            workshop.save()
        return workshop
