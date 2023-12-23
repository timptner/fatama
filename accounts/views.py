from django.views.generic import DetailView

from accounts.models import Profile


class ProfileView(DetailView):
    model = Profile
    template_name = 'accounts/user_detail.html'

    def get_object(self, queryset=None):
        return self.request.user
