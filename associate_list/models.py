from django.db import models

class Associate(models.Model):
    company_name = models.CharField(max_length=255)
    company_type = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=255)
    specialization = models.CharField(max_length=255)
    skills = models.TextField()
    phone_number = models.CharField(max_length=20)
    comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.company_name
