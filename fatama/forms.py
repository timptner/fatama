from django import forms
from django.forms.renderers import TemplatesSetting


class BulmaFormRenderer(TemplatesSetting):
    form_template_name = "fatama/form_snippet.html"
    formset_template_name = "fatama/formset_snippet.html"


class ModelForm(forms.ModelForm):
    template_name_label = "fatama/forms/label.html"


class Form(forms.Form):
    template_name_label = "fatama/forms/label.html"


class Select(forms.Select):
    template_name = "fatama/forms/widgets/select.html"


class FileInput(forms.FileInput):
    template_name = "fatama/forms/widgets/file.html"


class CheckboxInput(forms.CheckboxInput):
    template_name = "fatama/forms/widgets/checkbox.html"


class RadioSelect(forms.RadioSelect):
    template_name = "fatama/forms/widgets/radio.html"
    option_template_name = "fatama/forms/widgets/radio_option.html"
