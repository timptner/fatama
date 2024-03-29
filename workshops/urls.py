from django.urls import path

from . import views

app_name = "workshops"
urlpatterns = [
    path("", views.WorkshopListView.as_view(), name="workshop_list"),
    path("add/", views.WorkshopCreateView.as_view(), name="create_workshop"),
]
