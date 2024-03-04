from django.urls import path

from accounts import views

app_name = 'accounts'
urlpatterns = [
    path('council/add/', views.CouncilCreateView.as_view(), name='create_council'),
    path('councils/', views.CouncilListView.as_view(), name='council_list'),
    path('invite/', views.InviteCreateView.as_view(), name='create_invite'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('password/change/', views.PasswordChangeView.as_view(), name='edit_password'),
    path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirm.as_view(), name='password_reset_confirm'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/change/', views.UserUpdateView.as_view(), name='edit_profile'),
    path('register/<token>/', views.registration, name='register'),
]
