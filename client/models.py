from django.contrib.auth.models import User
from django.db import models
from lead.models import Lead

class CLient(models.Model):

    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'

    CHOICES_PRIORITY = (
        (LOW, 'Low'),
        (MEDIUM, 'Medium'),
        (HIGH, 'High'),
    )

    INACTIVE = 'inactive'
    PROSPECTING = 'prospecting'
    CONTACTED = 'contacted'
    PROPOSAL_SENT = 'proposal_sent'
    ACTIVE = 'active'
    ON_HOLD = 'on_hold'
    DELIVERED = 'delivered'
    POST_DEL = 'post_delivery_follow_up'
    CLOSED_SUCCESSFUL = 'closed_successful'
    CLOSED_UNSUCCESSFUL = 'closed_unsuccessful'

    CHOICES_STATUS = (
        (INACTIVE, 'Inactive'),
        (PROSPECTING, 'Prospecting'),
        (CONTACTED, 'Contacted'),
        (PROPOSAL_SENT, 'Proposal Sent'),
        (ACTIVE, 'Active'),
        (ON_HOLD, 'On Hold'),
        (DELIVERED, 'Delivered'),
        (POST_DEL, 'Post Delivery Follow Up'),
        (CLOSED_SUCCESSFUL, 'Closed Successful'),
        (CLOSED_UNSUCCESSFUL, 'Closed Unsuccessful'),

    )
    
    company = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=255)
    lead_consultant = models.CharField(max_length=255)
    priority = models.CharField(max_length=20, choices=CHOICES_PRIORITY, default=MEDIUM)
    deliverable_type = models.CharField(max_length=255)
    deliverable_name = models.CharField(max_length=255)
    status = models.CharField(max_length=30, choices=CHOICES_STATUS, default=INACTIVE)
    feedback = models.TextField(blank=True, null=True)
    start_date = models.DateField()
    next_followup = models.DateField()
    created_by = models.ForeignKey(User, related_name='clients', on_delete=models.CASCADE)

    def __str__(self):
        return self.company
