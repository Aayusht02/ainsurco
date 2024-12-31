from django.urls import path
from .views import calendar_view, add_attendance, export_attendance_csv

app_name = 'time_tracker'

urlpatterns = [
    path('', calendar_view, name='calendar_view'),  # Main calendar view
    path('add-attendance/<str:attendance_date>/', add_attendance, name='add_attendance'),  # Add attendance
    path('attendance/<int:user_id>/<int:month>/<int:year>/download/', export_attendance_csv, name='export_attendance_csv'),  # Export CSV
]
