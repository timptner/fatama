from django.conf import settings
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.auth import logout, views as auth_views
from django.core.exceptions import PermissionDenied
from django.http import request
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    FormView,
    ListView,
    TemplateView,
    UpdateView,
)

from accounts.forms import (
    AuthenticationForm,
    CouncilForm,
    InviteForm,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
    UserForm,
)
from accounts.models import Council, Invite


class CouncilCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = CouncilForm
    success_message = "Gremium wurde erfolgreich erstellt."
    success_url = reverse_lazy("accounts:council_list")
    template_name = "accounts/council_form.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class CouncilListView(LoginRequiredMixin, ListView):
    model = Council


class CouncilUpdateView(UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    form_class = CouncilForm
    success_message = "Gremium wurde aktualisiert."
    success_url = reverse_lazy("accounts:council_list")
    template_name = "accounts/council_form.html"

    def get_object(self, queryset=None):
        council = get_object_or_404(Council, pk=self.kwargs['pk'])
        return council

    def get_form_kwargs(self):
        council = get_object_or_404(Council, pk=self.kwargs['pk'])
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': council.owner})
        return kwargs

    def test_func(self):
        council = get_object_or_404(Council, pk=self.kwargs['pk'])
        if self.request.user == council.owner:
            return True
        else:
            return False


class InviteCreateView(PermissionRequiredMixin, SuccessMessageMixin, FormView):
    form_class = InviteForm
    permission_required = "accounts.can_invite"
    template_name = "accounts/create_invite.html"
    success_url = reverse_lazy("accounts:create_invite")
    success_message = "Einladungen wurde per E-Mail verschickt."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["expiration"] = settings.INVITE_EXPIRATION
        return context

    def get_form_kwargs(self) -> dict:
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save(self.request)
        return super().form_valid(form)


class LoginView(auth_views.LoginView):
    form_class = AuthenticationForm
    template_name = "accounts/login.html"


class LogoutView(auth_views.LogoutView):
    http_method_names = ["get", "post", "options"]
    next_page = reverse_lazy("accounts:login")
    template_name = "accounts/logout.html"

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return render(request, "accounts/logout.html")
        else:
            return redirect("accounts:login")


class PasswordChangeView(SuccessMessageMixin, auth_views.PasswordChangeView):
    form_class = PasswordChangeForm
    success_message = "Dein Password wurde aktualisiert."
    success_url = reverse_lazy("accounts:edit_password")
    template_name = "accounts/password_form.html"


class PasswordResetView(SuccessMessageMixin, auth_views.PasswordResetView):
    form_class = PasswordResetForm
    success_message = (
        "Eine E-Mail zum Zurücksetzen des Passworts wurde an <strong>%(email)s</strong> geschickt. Wenn "
        "innerhalb der nächsten 5 Minuten keine E-Mail zugestellt wurde existiert womöglich kein Konto "
        "mit dieser E-Mail-Adresse."
    )
    success_url = reverse_lazy("landing_page")
    template_name = "accounts/password_reset.html"


class PasswordResetConfirm(SuccessMessageMixin, auth_views.PasswordResetConfirmView):
    form_class = SetPasswordForm
    success_message = "Dein Passwort wurde erfolgreich geändert."
    success_url = reverse_lazy("accounts:login")
    template_name = "accounts/password_reset_confirm.html"


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/profile.html"


def registration(request, token):
    invite = get_object_or_404(Invite, token=token)
    if invite.is_expired():
        raise PermissionDenied("Invite is expired.")
    if request.method == "POST":
        user_form = UserForm(data=request.POST, prefix="user")
        password_form = SetPasswordForm(data=request.POST, user=None, prefix="password")
        if user_form.is_valid() and password_form.is_valid():
            user = user_form.save()
            logout(request)
            invite.delete()

            password_form.user = user
            password_form.save()

            return redirect(reverse_lazy("accounts:login"))
    else:
        if request.user.is_authenticated:
            message = (
                "Aktuell ist der Benutzer "
                f"<strong>{request.user}</strong> angemeldet. Bei "
                "Abschluss der Registrierung wird der aktive Benutzer "
                "abgemeldet."
            )
            messages.warning(request, message)
        password_form = SetPasswordForm(None, prefix="password")
        user_form = UserForm(prefix="user")
    return render(
        request,
        "accounts/registration.html",
        {
            "password_form": password_form,
            "user_form": user_form,
        },
    )


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    form_class = UserForm
    success_message = "Deine Informationen wurden aktualisiert."
    success_url = reverse_lazy("accounts:profile")
    template_name = "accounts/user_form.html"

    def get_object(self, queryset=None):
        return self.request.user
