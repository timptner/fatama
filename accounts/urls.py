from django.urls import path

from accounts import views

app_name = 'accounts'
urlpatterns = [
    path('invite/', views.InviteCreateView.as_view(), name='create_invite'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
]
