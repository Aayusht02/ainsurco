from django.contrib.auth.models import User
from django.db import models

class Lead(models.Model):

    LEAD_TYPE_CHOICES = [
        ('company', 'Company'),
        ('contact person', 'Contact Person'),
    ]
    
    lead_type = models.CharField(max_length=20, choices=LEAD_TYPE_CHOICES, default='company')
    company_type = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=255)
    roles = models.CharField(max_length=255)
    email = models.EmailField()
    region = models.CharField(max_length=255)
    linkedin_profile = models.URLField(max_length=200, blank=True, null=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)  
    comments = models.TextField(blank=True, null=True) 
    created_by = models.ForeignKey(User, related_name='leads', on_delete=models.CASCADE)

    def __str__(self):
        return self.company if self.lead_type == 'company' else self.contact_person
