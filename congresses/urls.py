from django.urls import path

from congresses import views

app_name = 'congresses'
urlpatterns = [
    path('', views.CongressesListView.as_view(), name='congress_list'),
]
