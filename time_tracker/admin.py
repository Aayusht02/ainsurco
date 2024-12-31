
import csv
from django.contrib import admin
from rangefilter.filters import DateRangeFilter
from django.http import HttpResponse
from .models import Attendance
from django.utils import timezone
from datetime import datetime

class MonthFilter(admin.SimpleListFilter):
    title = 'month' 
    parameter_name = 'month'  

    def lookups(self, request, model_admin):
        """Define the available months for filtering."""
        months = Attendance.objects.dates('date', 'month')  
        return [(month.month, month.strftime('%B')) for month in months]

    def queryset(self, request, queryset):
        """Filter the queryset based on the selected month."""
        if self.value():
            return queryset.filter(date__month=self.value())
        return queryset

class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('employee', 'date', 'status', 'overtime', 'department', 'comments')
    actions = ['export_as_csv']
    list_filter = ('employee', ('date', DateRangeFilter), MonthFilter) 

    def export_as_csv(self, request, queryset):
       
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="attendance.csv"'

        writer = csv.writer(response)
        writer.writerow(['Employee', 'Date', 'Status', 'Overtime', 'Department', 'Comments'])

        
        sorted_queryset = queryset.order_by('date')

        for attendance in sorted_queryset:
            writer.writerow([
                attendance.employee.username,
                attendance.date.strftime('%Y-%m-%d'),
                attendance.status,
                attendance.overtime,
                attendance.department,
                attendance.comments,
            ])

        return response

    export_as_csv.short_description = "Export Selected Attendance to CSV"

    def get_queryset(self, request):
        
        qs = super().get_queryset(request)
       
        if not request.GET:  
            last_31_days = timezone.now() - timezone.timedelta(days=31)
            return qs.filter(date__gte=last_31_days)
        return qs

    def changelist_view(self, request, extra_context=None):
       
        extra_context = extra_context or {}
        extra_context['title'] = 'Attendance Records' 
        return super().changelist_view(request, extra_context=extra_context)


admin.site.register(Attendance, AttendanceAdmin)
