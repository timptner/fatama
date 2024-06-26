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
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from accounts.models import Council, Invite, Profile
from fatama.forms import ModelForm, Form
from fatama.postmark import Mail


class AuthenticationForm(auth_forms.AuthenticationForm):
    template_name_label = "fatama/forms/label.html"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        fields = {
            "username": "Benutzername",
            "password": "Passwort",
        }
        for field, label in fields.items():
            self.fields[field].widget.attrs.update({"class": "input"})
            self.fields[field].label = label

        self.error_messages.update(
            {
                "invalid_login": (
                    "Die Kombination aus Benutzername und Passwort ist ungültig. Beachte bitte, dass beide Felder die "
                    "Groß- und Kleinschreibung berücksichtigen."
                ),
                "inactive": "Dieses Konto ist inaktiv.",
            }
        )


class CouncilForm(ModelForm):
    class Meta:
        model = Council
        fields = ["university", "name"]
        widgets = {
            "university": forms.TextInput(attrs={"class": "input"}),
            "name": forms.TextInput(attrs={"class": "input"}),
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
    emails = forms.CharField(
        label="E-Mail-Adressen",
        widget=forms.Textarea(attrs={"class": "textarea", "rows": 5}),
    )

    def __init__(self, user, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_emails(self) -> list[str]:
        data = self.cleaned_data["emails"]
        emails = [email.strip() for email in data.split(",")]
        for email in emails:
            try:
                validate_email(email)
            except ValidationError:
                raise ValidationError(
                    f"'{email}' ist keine gültige E-Mail-Adresse", code="invalid"
                )
        return emails

    @staticmethod
    def send_mail(request, invite: Invite) -> None:
        scheme = "https" if request.is_secure() else "http"
        host = request.get_host()
        path = reverse_lazy("accounts:register", kwargs={"token": invite.token})
        url = f"{scheme}://{host}{path}"

        context = {
            "action_url": url,
            "expired_at": invite.expired_at,
            "sender": invite.sender.get_full_name(),
        }

        mail = Mail(
            "invite",
            "Einladung zur FaTaMa",
            render_to_string("accounts/mails/invite.md", context, request),
            invite.recipient,
        )
        mail.send()

    def save(self, request) -> None:
        emails = self.cleaned_data["emails"]
        for email in emails:
            token = secrets.token_urlsafe(settings.INVITE_TOKEN_LENGTH)
            expired_at = timezone.now() + timedelta(days=settings.INVITE_EXPIRATION)
            invite = Invite.objects.create(
                token=token, recipient=email, sender=self.user, expired_at=expired_at
            )
            self.send_mail(request, invite)


class PasswordChangeForm(auth_forms.PasswordChangeForm):
    template_name_label = "fatama/forms/label.html"

    def __init__(self, user, *args, **kwargs) -> None:
        super().__init__(user, *args, **kwargs)
        fields = {
            "old_password": "Altes Passwort",
            "new_password1": "Neues Passwort",
            "new_password2": "Neues Passwort wiederholen",
        }
        for field, label in fields.items():
            self.fields[field].widget.attrs.update({"class": "input"})
            self.fields[field].label = label
        self.fields["new_password1"].help_text = "<br/>".join(
            [
                "Dein Passwort darf keine Ähnlichkeit zu anderen persönlichen Information aufweisen.",
                "Dein Passwort muss aus mindestens 8 Zeichen bestehen.",
                "Dein Passwort darf nicht zu offensichtlich sein.",
                "Dein Passwort darf nicht nur aus Ziffern bestehen.",
            ]
        )


class PasswordResetForm(auth_forms.PasswordResetForm):
    template_name_label = "fatama/forms/label.html"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update({"class": "input"})
        self.fields["email"].label = "E-Mail-Adresse"

    def send_mail(self, *args, **kwargs) -> None:
        request = kwargs["request"]
        token_generator = kwargs["token_generator"]
        user = kwargs["user"]
        scheme = "https" if request.is_secure() else "http"
        host = request.get_host()
        path = reverse_lazy(
            "accounts:password_reset_confirm",
            kwargs={
                "uidb64": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": token_generator.make_token(user),
            },
        )
        url = f"{scheme}://{host}{path}"

        context = {"action_url": url, "user": user}

        mail = Mail(
            "password-reset",
            "Zurücksetzen deines Passworts",
            render_to_string("accounts/mails/password_reset.md", context, request),
            user.email,
        )
        mail.send()

    def save(self, *args, **kwargs):
        email = self.cleaned_data["email"]
        request = kwargs["request"]
        token_generator = kwargs["token_generator"]
        for user in self.get_users(email):
            self.send_mail(request=request, token_generator=token_generator, user=user)


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
    template_name_label = "fatama/forms/label.html"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["new_password1"].widget.attrs.update({"class": "input"})
        self.fields["new_password2"].widget.attrs.update({"class": "input"})
        self.fields["new_password1"].help_text = "<br>".join(
            password_validators_help_texts()
        )


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]
        labels = {
            "username": "Benutzername",
            "first_name": "Vorname",
            "last_name": "Nachname",
            "email": "E-Mail-Adresse",
        }
        widgets = {
            "username": forms.TextInput(attrs={"class": "input"}),
            "first_name": forms.TextInput(attrs={"class": "input"}),
            "last_name": forms.TextInput(attrs={"class": "input"}),
            "email": forms.EmailInput(attrs={"class": "input"}),
        }
        help_texts = {
            "username": "150 Zeichen oder weniger. Buchstaben und Ziffern sind zulässig.",
            "email": "Deine persönliche E-Mail-Adresse. Bitte nicht die E-Mail-Adresse der Fachschaft angeben.",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].required = True
        self.fields["last_name"].required = True
        self.fields["email"].required = True

    def clean_username(self):
        username = self.cleaned_data.get("username")
        match = re.match(r"^[a-z\d]+$", username, re.IGNORECASE)
        if not match:
            raise ValidationError(
                "Es sind nur Buchstaben und Ziffern erlaubt.", code="blocked_symbol"
            )
        return username
