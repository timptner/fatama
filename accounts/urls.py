from django.urls import path

from accounts import views

app_name = 'accounts'
urlpatterns = [
    path('invite/', views.InviteCreateView.as_view(), name='create_invite'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirm.as_view(), name='password_reset_confirm'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('register/<token>/', views.registration, name='register'),
]
