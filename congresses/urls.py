from django.urls import path

from congresses import views

app_name = 'congresses'
urlpatterns = [
    path('', views.CongressesListView.as_view(), name='congress_list'),
    path('<int:congress_id>/participants/', views.ParticipantListView.as_view(), name='participant_list'),
]
