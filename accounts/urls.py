from django.urls import path

from accounts import views

app_name = 'accounts'
urlpatterns = [
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('invite/', views.InviteCreateView.as_view(), name='create_invite'),
]
