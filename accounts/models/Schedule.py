from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime

class Schedule(models.Model):
    # Define model fields.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    start_time = models.TimeField(auto_now=False, auto_now_add=False, default=datetime.time(7, 00))
    end_time = models.TimeField(auto_now=False, auto_now_add=False, default=datetime.time(16, 00))
    hours_per_day = models.IntegerField(default=8)
    works_monday = models.BooleanField(default=True)
    works_tuesday = models.BooleanField(default=True)
    works_wednesday = models.BooleanField(default=True)
    works_thursday = models.BooleanField(default=True)
    works_friday = models.BooleanField(default=True)
    works_saturday = models.BooleanField(default=False)
    works_sunday = models.BooleanField(default=False)

    # Used internally to display the string represention of the object.
    def __str__(self):
        return self.user.username
    # Listens for user activity.
    @receiver(post_save, sender=User)
    # When user is created, this will attach a profile to the user.
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Schedule.objects.create(user=instance)
    # When user is saved, this will save the profile as well.
    def save_user_profile(sender, instance, **kwargs):
        instance.schedule.save()
    # Determine which day to check
    def check_schedule(self, isoday):
        if isoday == 1:
            return self.works_monday
        elif isoday == 2:
            return self.works_tuesday
        elif isoday == 3:
            return self.works_wednesday
        elif isoday == 4:
            return self.works_thursday
        elif isoday == 5:
            return self.works_friday
        elif isoday == 6:
            return self.works_saturday
        elif isoday == 7:
            return self.works_sunday
        else:
            pass # Throw error
