from django.urls import path

from congresses import views

app_name = 'congresses'
urlpatterns = [
    path('<int:year>', views.CongressDetailView.as_view(), name='congress_detail'),
    path('attendances/<int:pk>/', views.AttendanceDetailsView.as_view(), name='attendance-detail'),
    path('attendances/<int:pk>/add_participant/', views.ParticipantCreateView.as_view(), name='create-participant'),
    path('congresses/', views.CongressListView.as_view(), name='congress-list'),
    path('congresses/<int:pk>/', views.CongressDetailView.as_view(), name='congress-detail'),
    path('congresses/<int:pk>/add_attendance/', views.AttendanceCreateView.as_view(), name='create-attendance'),
    path('participants/<int:pk>/add_portrait/', views.PortraitCreateView.as_view(), name='create-portrait'),
    path('attendances/update_seats/', views.SeatFormView.as_view(), name='update-seats'),
]
