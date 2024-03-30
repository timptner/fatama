from django.urls import path

from excursions import views

app_name = "excursions"
urlpatterns = [
    path("", views.ExcursionListView.as_view(), name="excursion_list"),
]
