from django import forms
from .models import Associate

class AssociateForm(forms.ModelForm):
    class Meta:
        model = Associate
        fields = ['company_name', 'company_type', 'contact_person', 'specialization', 'skills', 'phone_number', 'comments']
