import secrets

from datetime import timedelta

from django import forms
from django.conf import settings
from django.contrib.auth import forms as auth_forms
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.utils import timezone

from accounts.models import Invite, Profile


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


class PasswordResetForm(auth_forms.PasswordResetForm):
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


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['university']
        widgets = {
            'university': forms.TextInput(attrs={'class': 'input'})
        }

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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].widget.attrs.update({'class': 'input'})
        self.fields['new_password2'].widget.attrs.update({'class': 'input'})


class UserForm(forms.ModelForm):
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
