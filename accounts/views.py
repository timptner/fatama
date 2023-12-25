from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth import views as auth_views
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView

from accounts.forms import InviteForm, AuthenticationForm


class LoginView(auth_views.LoginView):
    form_class = AuthenticationForm
    template_name = 'accounts/login.html'


class LogoutView(auth_views.LogoutView):
    http_method_names = ['get', 'post', 'options']
    next_page = reverse_lazy('accounts:login')
    template_name = 'accounts/logout.html'

    def get(self, request, *args, **kwargs):
        return render(request, 'accounts/logout.html')


class ProfileView(TemplateView):
    template_name = 'accounts/profile.html'


class InviteCreateView(PermissionRequiredMixin, CreateView):
    form_class = InviteForm
    permission_required = 'accounts.can_invite'
    template_name = 'accounts/create_invite.html'

    def get_form_kwargs(self) -> dict:
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form) -> None:
        form.send_email()
        return super().form_valid(form)
