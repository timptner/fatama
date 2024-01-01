import secrets

from datetime import timedelta

from django import forms
from django.conf import settings
from django.contrib.auth import forms as auth_forms
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.utils import timezone

from accounts.models import Council, Invite, Profile
from fatama.forms import ModelForm


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


class InviteForm(ModelForm):
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
