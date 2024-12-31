# client/forms.py

from django import forms
from .models import CLient
from lead.models import Lead

class AddClientForm(forms.ModelForm):
    company = forms.ChoiceField(choices=[])
    contact_person = forms.ChoiceField(choices=[])

    class Meta:
        model = CLient
        fields = (
            'company', 'contact_person', 'lead_consultant', 'priority',
            'deliverable_type', 'deliverable_name', 'status',
            'feedback', 'start_date', 'next_followup',
        )
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'next_followup': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        }

    def __init__(self, *args, **kwargs):
        selected_company = kwargs.pop('selected_company', None)
        super().__init__(*args, **kwargs)

        
        companies = Lead.objects.values_list('company', flat=True).distinct()
        self.fields['company'].choices = [(company, company) for company in companies]

        
        if selected_company:
            self.fields['company'].initial = selected_company
        elif self.instance and self.instance.company:
            self.fields['company'].initial = self.instance.company

        
        selected_company = selected_company or self.data.get('company')
        if selected_company:
            contact_persons = Lead.objects.filter(company=selected_company).values_list('contact_person', flat=True).distinct()
            self.fields['contact_person'].choices = [(person, person) for person in contact_persons]
        else:
            self.fields['contact_person'].choices = []

    def clean(self):
        cleaned_data = super().clean()
        company = cleaned_data.get('company')
        contact_person = cleaned_data.get('contact_person')

       
        if company not in dict(self.fields['company'].choices):
            self.add_error('company', "Select a valid choice for the company.")

        
        if company and contact_person:
            contact_persons = Lead.objects.filter(company=company).values_list('contact_person', flat=True).distinct()
            if contact_person not in [person for person in contact_persons]:
                self.add_error('contact_person', "Select a valid choice for the contact person.")

        return cleaned_data


        
        if self.instance.pk:  
            if self.instance.start_date:
                self.initial['start_date'] = self.instance.start_date.strftime('%Y-%m-%d')
            if self.instance.next_followup:
                self.initial['next_followup'] = self.instance.next_followup.strftime('%Y-%m-%d')
            
            
            self.fields['start_date'].widget.attrs['readonly'] = True