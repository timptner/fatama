import secrets

from datetime import timedelta

from django import forms
from django.conf import settings
from django.contrib.auth import forms as auth_forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth import password_validation
from django.utils import timezone

from accounts.models import Invite


class AuthenticationForm(auth_forms.AuthenticationForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'input'})
        self.fields['password'].widget.attrs.update({'class': 'input'})


class InviteForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs) -> None:
        self.user = user
        super().__init__(*args, **kwargs)

    class Meta:
        model = Invite
        fields = ['recipient']
        widgets = {
            'recipient': forms.EmailInput(attrs={'class': 'input'}),
        }

    def save(self, commit: bool = True) -> Invite:
        token = secrets.token_urlsafe(settings.INVITE_TOKEN_LENGTH)
        expired_at = timezone.now() + timedelta(days=settings.INVITE_EXPIRATION)
        invite = super().save(commit=False)
        invite.token = token
        invite.sender = self.user
        invite.expired_at = expired_at
        if commit:
            invite.save()
        return invite


class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Passwort",
        widget=forms.PasswordInput(attrs={'class': 'input', "autocomplete": "new-password"}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label="Passwort bestätigen",
        widget=forms.PasswordInput(attrs={'class': 'input', "autocomplete": "new-password"}),
        strip=False,
    )

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True

    def clean_password1(self) -> str:
        password1 = self.cleaned_data.get('password1')
        password_validation.validate_password(password1)
        return password1

    def clean(self) -> None:
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            error = ValidationError("Die Passwörter sind nicht identisch.", code='distinct_passwords')
            self.add_error('password2', error)

    def save(self, commit: bool = True) -> User:
        if not commit:
            raise NotImplementedError("Must commit user object to set new password afterwards.")
        password = self.cleaned_data['password1']
        user: User = super().save(commit=False)
        user.set_password(password)
        user.is_active = True
        user.save()
        return user
