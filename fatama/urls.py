from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('accounts/', include('accounts.urls')),
    path('congresses/', include('congresses.urls')),
    path('admin/', admin.site.urls),
]
