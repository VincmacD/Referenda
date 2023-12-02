from django.contrib import admin
from .models import Voter, Vote, Referendum, Choice, User

# Register your models here.

admin.site.register(Voter)
admin.site.register(Vote)
admin.site.register(Referendum)
admin.site.register(Choice)
admin.site.register(User)