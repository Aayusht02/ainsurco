# time_tracker/models.py
from django.db import models
from django.contrib.auth.models import User

class Attendance(models.Model):
    STATUS_CHOICES = [
        ('full_day', 'Full Day'),
        ('half_day', 'Half Day'),
        ('leave', 'Leave'),
    ]

    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(unique=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    overtime = models.FloatField(default=0)
    department = models.CharField(max_length=100, blank=True)
    comments = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('employee', 'date')  # Ensure unique attendance per user per date

    def __str__(self):
        return f"{self.employee.username} - {self.date} - {self.status}"