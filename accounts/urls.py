from django.urls import path

from accounts import views

app_name = 'accounts'
urlpatterns = [
    path('invite/', views.InviteCreateView.as_view(), name='create_invite'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('register/<str:token>/', views.RegistrationView.as_view(), name='register'),
]
