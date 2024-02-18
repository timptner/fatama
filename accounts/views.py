from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth import logout, views as auth_views
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, TemplateView

from accounts.forms import (AuthenticationForm, CouncilForm, InviteForm,
                            PasswordResetForm, SetPasswordForm, UserForm)
from accounts.models import Council, Invite


class CouncilCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = CouncilForm
    success_message = "Gremium wurde erfolgreich erstellt."
    success_url = reverse_lazy('accounts:council_list')
    template_name = 'accounts/council_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class CouncilListView(LoginRequiredMixin, ListView):
    model = Council


class InviteCreateView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = InviteForm
    permission_required = 'accounts.can_invite'
    template_name = 'accounts/create_invite.html'
    success_url = reverse_lazy('accounts:create_invite')
    success_message = "Einladung wurde per E-Mail an <strong>%(recipient)s</strong> verschickt."

    def get_form_kwargs(self) -> dict:
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        response = super().form_valid(form)
        self.send_mail()
        return response

    def send_mail(self) -> None:
        invite: Invite = self.object
        name = invite.sender.get_full_name()
        scheme = 'https' if self.request.is_secure() else 'http'
        host = self.request.get_host()
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


class LoginView(auth_views.LoginView):
    form_class = AuthenticationForm
    template_name = 'accounts/login.html'


class LogoutView(auth_views.LogoutView):
    http_method_names = ['get', 'post', 'options']
    next_page = reverse_lazy('accounts:login')
    template_name = 'accounts/logout.html'

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return render(request, 'accounts/logout.html')
        else:
            return redirect('accounts:login')


class PasswordResetView(SuccessMessageMixin, auth_views.PasswordResetView):
    form_class = PasswordResetForm
    success_message = "Eine E-Mail zum Zurücksetzen des Passworts wurde an <strong>%(email)s</strong> geschickt."
    success_url = reverse_lazy('accounts:login')
    template_name = 'accounts/password_reset.html'


class PasswordResetConfirm(SuccessMessageMixin, auth_views.PasswordResetConfirmView):
    form_class = SetPasswordForm
    success_message = "Dein Passwort wurde erfolgreich geändert."
    success_url = reverse_lazy('accounts:login')
    template_name = 'accounts/password_reset_confirm.html'


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'


def registration(request, token):
    invite = get_object_or_404(Invite, token=token)
    if invite.is_expired():
        raise PermissionDenied("Invite is expired.")
    if request.method == 'POST':
        user_form = UserForm(data=request.POST, prefix='user')
        password_form = SetPasswordForm(data=request.POST, user=None, prefix='password')
        if user_form.is_valid() and password_form.is_valid():
            user = user_form.save()
            logout(request)
            invite.delete()

            password_form.user = user
            password_form.save()

            return redirect(reverse_lazy('accounts:login'))
    else:
        if request.user.is_authenticated:
            message = ("Aktuell ist der Benutzer "
                       f"<strong>{request.user}</strong> angemeldet. Bei "
                       "Abschluss der Registrierung wird der aktive Benutzer "
                       "abgemeldet.")
            messages.warning(request, message)
        password_form = SetPasswordForm(None, prefix='password')
        user_form = UserForm(prefix='user')
    return render(request, 'accounts/registration.html', {
        'password_form': password_form,
        'user_form': user_form,
    })
