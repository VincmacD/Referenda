from django.db.models.signals import post_save
from .models import User
from .models import Voter
from django.contrib.auth.models import Group


def Voter_profile(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name="voters")
        instance.groups.add(group)
        Voter.objects.create(
            user=instance, username=instance.username, email=instance.email
        )


post_save.connect(Voter_profile, sender=User)
