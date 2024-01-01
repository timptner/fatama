from django.contrib import admin
from django.urls import path, include, reverse
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda request: redirect(reverse('congresses:congress-list'))),
    path('', include('congresses.urls')),
    path('accounts/', include('accounts.urls')),
    path('admin/', admin.site.urls),
]
