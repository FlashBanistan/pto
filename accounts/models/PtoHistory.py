from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class PtoHistory(models.Model):
    LEAVE_CHOICES = (
        ('pto', 'PTO'),
        ('jury_duty', 'Jury Duty'),
        ('voting', 'Voting'),
        ('military_leave', 'Military Leave'),
        ('bereavement', 'Bereavement'),
        ('emergency', 'Emergency'),
    )
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('denied', 'Denied'),
        ('cancelled', 'Cancelled'),
    )
    # Define model fields.
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(null=True, blank=True, editable=False, max_length=20)
    start = models.DateTimeField(auto_now=False, auto_now_add=False)
    end = models.DateTimeField(auto_now=False, auto_now_add=False)
    leave_type = models.CharField(choices=LEAVE_CHOICES, max_length=100)
    is_chargeable = models.BooleanField(default=False, editable=False)
    status = models.CharField(choices=STATUS_CHOICES, default='pending', max_length=15)
    # Used internally in the django admin to display the string representation of the object.
    def __str__(self):
        return self.user.username
    # Runs whenever a PtoHistory is saved to determine if the leave_type is chargeable or not.
    def save(self, *args, **kwargs):
        if self.leave_type == 'pto' or self.leave_type == 'emergency':
            self.is_chargeable = True
        else:
            self.is_chargeable = False
        super().save(*args, **kwargs)
