import secrets

from datetime import datetime, timedelta

from django import forms
from django.contrib.auth import forms as auth_forms
from django.core.mail import send_mail

from accounts.models import Invite


class InviteForm(forms.ModelForm):
    def __init__(self, *args, **kwargs) -> None:
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    class Meta:
        model = Invite
        fields = ['recipient']
        widgets = {
            'recipient': forms.EmailInput(attrs={'class': 'input'}),
        }

    def save(self, commit: bool = True) -> None:
        invite = super().save(commit=False)
        invite.token = secrets.token_urlsafe(10)
        invite.sender = self.user
        invite.expired_at = datetime.utcnow() + timedelta(days=10)
        if commit:
            invite.save()
        return invite

    def send_email(self) -> None:
        recipient = self.cleaned_data['recipient']
        sender = self.user.get_full_name() or self.user.username
        send_mail(
            "Einladung zur FaTaMa2024",
            f"""Hallo,

du wurdest von {sender} eingeladen, dich für die Fachschaftentagung Maschinenbau 2024 zu registrieren.""",
            None,
            [recipient],
        )


class AuthenticationForm(auth_forms.AuthenticationForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'input'})
        self.fields['password'].widget.attrs.update({'class': 'input'})
