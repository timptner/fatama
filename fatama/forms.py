from django import forms
from django.forms.renderers import TemplatesSetting


class BulmaFormRenderer(TemplatesSetting):
    form_template_name = "fatama/form_snippet.html"


class ModelForm(forms.ModelForm):
    template_name_label = "fatama/forms/label.html"


class Form(forms.Form):
    template_name_label = "fatama/forms/label.html"


class Select(forms.Select):
    template_name = "fatama/forms/widgets/select.html"


class FileInput(forms.FileInput):
    template_name = "fatama/forms/widgets/file.html"
