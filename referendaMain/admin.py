from django.contrib import admin

# Register your models here.

from .models import Voter, Vote, Referendum, Choice

admin.site.register(Voter)
admin.site.register(Vote)
admin.site.register(Referendum)
admin.site.register(Choice)