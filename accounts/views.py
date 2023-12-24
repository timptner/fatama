from django.views.generic import TemplateView

from accounts.models import Profile

class ProfileView(TemplateView):
    template_name = 'accounts/profile.html'


    def get_object(self, queryset=None):
        return self.request.user
