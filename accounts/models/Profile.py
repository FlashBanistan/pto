from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    PTO_TIER_CHOICES = (
        (200.0, 'Boss 5-10 Years'),
        (160.0, 'Boss 2-5 Years'),
        (120.0, 'Boss 0-2 Years'),
        (160.0, 'Peon 5-10 Years'),
        (120.0, 'Peon 2-5 Years'),
        (90.0, 'Peon 0-2 Years'),
    )
    # Define model fields.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pto_tier = models.FloatField(choices=PTO_TIER_CHOICES, default=90.0)
    # Used internally to display the string represention of the object.
    def __str__(self):
        return self.user.username
    # Listens for user activity.
    @receiver(post_save, sender=User)
    # When user is created, this will attach a profile to the user.
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
    # When user is saved, this will save the profile as well.
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
