from django import forms
from .models import CLient
from lead.models import Lead

class AddClientForm(forms.ModelForm):
    
    class Meta:
        model = CLient
        fields = (
            'company', 'contact_person', 'lead_consultant', 'priority', 
            'deliverable_type', 'deliverable_name', 'status', 
            'feedback', 'start_date', 'next_followup',
        )
        widgets = {
            'start_date': forms.DateInput(
                attrs={'type': 'date', 'class': 'bordered-field short-field'},
                format='%Y-%m-%d'
            ),
            'next_followup': forms.DateInput(
                attrs={'type': 'date', 'class': 'bordered-field short-field'},
                format='%Y-%m-%d'
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Populate the initial values for the date fields
        if self.instance.pk:  # Only if this is an existing instance
            if self.instance.start_date:
                self.initial['start_date'] = self.instance.start_date.strftime('%Y-%m-%d')
            if self.instance.next_followup:
                self.initial['next_followup'] = self.instance.next_followup.strftime('%Y-%m-%d')
            
            # Make start_date read-only
            self.fields['start_date'].widget.attrs['readonly'] = True