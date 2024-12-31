from django.shortcuts import render, redirect, get_object_or_404
from .models import Attendance
from datetime import datetime, date
from django.utils.dateformat import DateFormat
from django.http import HttpResponse
from django.contrib import messages
from .forms import AttendanceForm
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
import csv
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
import json


def calendar_view(request):
    today = date.today()
    
    attendance_records = Attendance.objects.filter(date__year=today.year, date__month=today.month)
    
    # Prepare attendance_status as a dictionary
    attendance_status = {
        DateFormat(record.date).format('Y-m-d'): record.status for record in attendance_records
    }

    # Pass serialized JSON to template
    return render(request, 'time_tracker/calendar.html', {
        'attendance_status': mark_safe(json.dumps(attendance_status)),  # Serialize JSON for frontend
        'today': today,
    })


@login_required
def add_attendance(request, attendance_date):
    """
    View to add or update attendance for a specific date.
    """
    try:
        # Parse the date string from the URL
        attendance_date = datetime.strptime(attendance_date, "%Y-%m-%d").date()
    except ValueError:
        messages.error(request, 'Invalid date format.')
        return redirect('time_tracker:calendar_view')

    # Fetch or create an attendance record for the given date and user
    try:
        attendance_record, created = Attendance.objects.get_or_create(
            date=attendance_date,
            employee=request.user
        )
    except IntegrityError:
        messages.error(request, 'Attendance record could not be created.')
        return redirect('time_tracker:calendar_view')

    # Handle form submission
    if request.method == 'POST':
        form = AttendanceForm(request.POST, instance=attendance_record)
        if form.is_valid():
            form.save()
            messages.success(request, 'Attendance updated successfully.')
            return redirect('time_tracker:calendar_view')
    else:
        form = AttendanceForm(instance=attendance_record)

    context = {
        'date': attendance_date,
        'form': form,
    }
    return render(request, 'time_tracker/add_attendance.html', context)


@login_required
def export_attendance_csv(request, user_id, month, year):
    """
    View to export attendance data as a CSV file for a specific user and month/year.
    """
    # Fetch the user
    user = get_object_or_404(User, id=user_id)

    # Fetch attendance records for the user and the specified month/year
    attendances = Attendance.objects.filter(employee=user, date__year=year, date__month=month)

    # Prepare the CSV response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{user.username}_attendance_{month}_{year}.csv"'

    writer = csv.writer(response)

    # Write the CSV header
    writer.writerow(['Employee', 'Date', 'Status', 'Overtime', 'Department', 'Comments'])

    # Write attendance rows
    for attendance in attendances:
        writer.writerow([
            attendance.employee.username,  # Employee username
            attendance.date.strftime('%b. %d, %Y'),  # Date in a readable format
            attendance.get_status_display(),  # Human-readable status
            attendance.overtime,  # Overtime hours
            attendance.department,  # Department name
            attendance.comments,  # Additional comments
        ])

    return response
