from django.urls import path

from congresses import views

app_name = 'congresses'
urlpatterns = [
    path('congresses/', views.CongressesListView.as_view(), name='congress_list'),
    path('congresses/<int:congress_id>/add_participant/',
         views.ParticipantCreateView.as_view(),
         name='create_participant'),
    path('congresses/<int:congress_id>/participants/', views.ParticipantListView.as_view(), name='participant_list'),
    path('participants/<int:participant_id>/add_profile/',
         views.PortraitCreateView.as_view(),
         name='create_portrait'),
]
