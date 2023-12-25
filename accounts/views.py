from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import TemplateView, CreateView

from accounts.forms import InviteForm


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
