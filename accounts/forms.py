import re
import secrets

from datetime import timedelta

from django import forms
from django.conf import settings
from django.contrib.auth import forms as auth_forms
from django.contrib.auth.password_validation import password_validators_help_texts
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.utils import timezone

from accounts.models import Council, Invite, Profile
from fatama.forms import ModelForm, Form


class AuthenticationForm(auth_forms.AuthenticationForm):
    template_name_label = 'fatama/forms/label.html'

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'input'})
        self.fields['password'].widget.attrs.update({'class': 'input'})


class CouncilForm(ModelForm):
    class Meta:
        model = Council
        fields = ['university', 'name']
        widgets = {
            'university': forms.TextInput(attrs={'class': 'input'}),
            'name': forms.TextInput(attrs={'class': 'input'}),
        }

    def __init__(self, user, *args, **kwargs) -> None:
        self.user = user
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        council = super().save(commit=False)
        council.owner = self.user
        if commit:
            council.save()
        return council


class InviteForm(Form):
    emails = forms.CharField(label="E-Mail-Adressen", widget=forms.Textarea(attrs={'class': 'textarea', 'rows': 5}))

    def __init__(self, user, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_emails(self) -> list[str]:
        data = self.cleaned_data['emails']
        emails = [email.strip() for email in data.split(',')]
        for email in emails:
            try:
                validate_email(email)
            except ValidationError:
                raise ValidationError(f"'{email}' ist keine gültige E-Mail-Adresse", code='invalid')
        return emails

    @staticmethod
    def send_mail(request, invite: Invite) -> None:
        name = invite.sender.get_full_name()
        scheme = 'https' if request.is_secure() else 'http'
        host = request.get_host()
        path = reverse_lazy('accounts:register', kwargs={'token': invite.token})
        url = f'{scheme}://{host}{path}'
        send_mail(
            "Einladung zur FaTaMa2024",
            f"""Hallo,

du wurdest von {name} eingeladen, dich für die Fachschaftentagung Maschinenbau 2024 zu registrieren.

{url}

Die Einladung ist bis {invite.expired_at} gültig.""",
            None,
            [invite.recipient],
        )

    def save(self, request) -> None:
        emails = self.cleaned_data['emails']
        for email in emails:
            token = secrets.token_urlsafe(settings.INVITE_TOKEN_LENGTH)
            expired_at = timezone.now() + timedelta(days=settings.INVITE_EXPIRATION)
            invite = Invite.objects.create(token=token, recipient=email, sender=self.user, expired_at=expired_at)
            self.send_mail(request, invite)


class PasswordResetForm(auth_forms.PasswordResetForm):
    template_name_label = 'fatama/forms/label.html'

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'input'})

    def send_mail(self, subject_template_name, email_template_name, context,
                  from_email, to_email, html_email_template_name=None):
        user = context.get('user')
        protocol = context.get('protocol')
        domain = context.get('domain')
        uid = context.get('uid')
        token = context.get('token')
        path = reverse_lazy('accounts:password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
        subject = "Password zurücksetzen"
        body = f"""Hallo {user.first_name},

du hast das Zurücksetzen deines Passworts angefordert.

{protocol}://{domain}{path}"""
        send_mail(subject, body, None, [to_email])


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = []

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        profile = super().save(commit=False)
        profile.user = self.user
        if commit:
            profile.save()
        return profile


class SetPasswordForm(auth_forms.SetPasswordForm):
    template_name_label = 'fatama/forms/label.html'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].widget.attrs.update({'class': 'input'})
        self.fields['new_password2'].widget.attrs.update({'class': 'input'})
        self.fields['new_password1'].help_text = '<br>'.join(password_validators_help_texts())


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {
            'username': "Benutzername",
            'first_name': "Vorname",
            'last_name': "Nachname",
            'email': "E-Mail-Adresse",
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'input'}),
            'first_name': forms.TextInput(attrs={'class': 'input'}),
            'last_name': forms.TextInput(attrs={'class': 'input'}),
            'email': forms.EmailInput(attrs={'class': 'input'}),
        }
        help_texts = {
            'username': "150 Zeichen oder weniger. Buchstaben und Ziffern sind zulässig."
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True

    def clean_username(self):
        username = self.cleaned_data.get('username')
        match = re.match(r'^[a-z\d]+$', username, re.IGNORECASE)
        if not match:
            raise ValidationError("Es sind nur Buchstaben und Ziffern erlaubt.", code='blocked_symbol')
        return username
