from django import forms

from .models import Lead

class AddLeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ('company_type', 'company', 'contact_person', 'roles', 'email', 'region', 'linkedin_profile', 'resume',)