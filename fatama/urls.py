from django.contrib import admin
from django.urls import path, include

from django.contrib.flatpages import views

urlpatterns = [
    path('', views.flatpage, {'url': '/'}, name='landing_page'),
    path('accounts/', include('accounts.urls')),
    path('admin/', admin.site.urls),
    path('congresses/', include('congresses.urls')),
    path('privacy/', views.flatpage, {'url': '/privacy/'}, name='privacy'),
    path('site-notice/', views.flatpage, {'url': '/site-notice/'}, name='site_notice'),
]
