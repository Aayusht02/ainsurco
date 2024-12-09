from django import forms
from django.contrib import admin
from .models import CLient
from lead.models import Lead

class CLientAdminForm(forms.ModelForm):
    class Meta:
        model = CLient
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['company'].queryset = Lead.objects.values_list('company', flat=True).distinct()
        self.fields['contact_person'].queryset = Lead.objects.values_list('contact_person', flat=True).distinct()

class CLientAdmin(admin.ModelAdmin):
    form = CLientAdminForm

admin.site.register(CLient, CLientAdmin)