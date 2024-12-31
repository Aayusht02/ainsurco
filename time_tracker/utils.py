# time_tracker/utils.py
import pandas as pd
from .models import Attendance
from django.http import HttpResponse

def generate_attendance_spreadsheet(year, month):
    # Fetch attendance records for the specified month
    attendance_records = Attendance.objects.filter(date__year=year, date__month=month)

    # Create a DataFrame
    data = {
        'Employee': [],
        'Date': [],
        'Status': [],
        'Overtime': [],
        'Department': [],
        'Comments': []
    }

    for record in attendance_records:
        data['Employee'].append(record.employee.username)
        data['Date'].append(record.date)
        data['Status'].append(record.status)
        data['Overtime'].append(record.overtime)
        data['Department'].append(record.department)
        data['Comments'].append(record.comments)

    df = pd.DataFrame(data)

    # Create an Excel file
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="attendance_{year}_{month}.xlsx"'
    
    # Write the DataFrame to the response
    df.to_excel(response, index=False)

    return response