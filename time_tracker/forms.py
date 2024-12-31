
from django import forms
from .models import Attendance

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['status', 'overtime', 'department', 'comments']
        widgets = {
            'comments': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'overtime': forms.NumberInput(attrs={'step': 0.1}),
            'department': forms.TextInput(attrs={'placeholder': 'Enter your department'}),
        }