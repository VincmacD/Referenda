from django.utils import timezone
import uuid
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.

class Voter(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    username = first_name = models.CharField(max_length=200, null=True)
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return str(self.user)
    
class Choice(models.Model):
    name = models.CharField(max_length=20)
    def __str__(self):
        return self.name
    
class Referendum(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200, null=True)
    description = models.CharField(max_length=500, null=True)
    choices = models.ManyToManyField(Choice, blank=True)
    date_published = models.DateField(default=timezone.now())
    date_available = models.DateField(null = True)
    date_expired = models.DateField(null = True)

    def __str__(self):
        return str(self.title)

class Vote(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    voter = models.ForeignKey(Voter, null=True, on_delete=models.SET_NULL)
    referendum = models.ForeignKey(Referendum, null=True, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.SET_NULL, null = True, blank = True)
    timestamp = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return f"{self.referendum.title} - {self.choice.name}"

