from django.urls import path

from congresses import views
from excursions.views import create_order

app_name = "congresses"
urlpatterns = [
    path("<int:year>/", views.CongressDetailView.as_view(), name="congress_detail"),
    path(
        "<int:year>/add_attendance/",
        views.AttendanceCreateView.as_view(),
        name="create_attendance",
    ),
    path("attendances/", views.AttendanceListView.as_view(), name="attendance_list"),
    path(
        "attendances/export/",
        views.AttendanceExportView.as_view(),
        name="attendance_export",
    ),
    path(
        "attendances/<int:pk>/",
        views.AttendanceDetailsView.as_view(),
        name="attendance_detail",
    ),
    path(
        "attendances/<int:pk>/add_participant/",
        views.ParticipantCreateView.as_view(),
        name="create_participant",
    ),
    path(
        "participants/<int:pk>/add_portrait/",
        views.PortraitCreateView.as_view(),
        name="create_portrait",
    ),
    path("participants/<int:pk>/add_excursion/", create_order, name="create_order"),
    path("update_seats/", views.SeatFormView.as_view(), name="update_seats"),
]
