from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth import login, views as auth_views
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from accounts.forms import AuthenticationForm, InviteForm, RegistrationForm
from accounts.models import Invite


class InviteCreateView(PermissionRequiredMixin, CreateView):
    form_class = InviteForm
    permission_required = 'accounts.can_invite'
    template_name = 'accounts/create_invite.html'
    success_url = reverse_lazy('accounts:create_invite')

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


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'


class RegistrationView(CreateView):
    form_class = RegistrationForm
    template_name = 'accounts/registration.html'
    success_url = reverse_lazy('accounts:profile')

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            message = ("Aktuell ist der Benutzer "
                       f"<strong>{self.request.user}</strong> angemeldet. Bei "
                       "Abschluss der Registrierung wird der aktive Benutzer "
                       "abgemeldet und der neue Benutzer stattdessen "
                       "angemeldet.")
            messages.warning(self.request, message)
        token = self.kwargs.get('token')
        invite = get_object_or_404(Invite, token=token)
        if invite.is_expired():
            raise PermissionDenied("Invite is expired.")
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response
