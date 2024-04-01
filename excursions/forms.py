from django import forms
from django.core.exceptions import ValidationError
from django.forms import BaseFormSet, formset_factory

from excursions.models import Order
from fatama.forms import Form, ModelForm, Select


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ["excursion"]
        widgets = {
            "excursion": Select(),
        }

    def __init__(self, *args, **kwargs):
        self.participant = kwargs.pop("participant")
        self.priority = kwargs.pop("priority")
        super().__init__(*args, **kwargs)
        self.fields["excursion"].label = f"Priorität {self.priority}"

    def save(self, commit=True):
        order = super().save(commit=False)
        order.participant = self.participant
        order.priority = self.priority
        if commit:
            order.save()
        return order


class BaseOrderFormSet(BaseFormSet):
    def get_form_kwargs(self, index):
        kwargs = super().get_form_kwargs(index)
        kwargs["priority"] = index + 1
        return kwargs

    def clean(self):
        excursions = set()
        if any(self.errors):
            return
        for form in self.forms:
            excursion = form.cleaned_data.get("excursion")
            if excursion.pk in excursions:
                raise ValidationError(
                    "Es müssen unterschiedliche Exkursionen ausgewählt werden. (%(excursion)s)",
                    params={"excursion": excursion},
                    code="duplicate",
                )
            excursions.add(excursion.pk)


OrderFormSet = formset_factory(OrderForm, extra=3, formset=BaseOrderFormSet)
