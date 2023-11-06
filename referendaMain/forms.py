from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Voter
from referendaMain.models import Referendum
from django.contrib.auth.forms import UserChangeForm

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1','password2']
    
class ReferendumForm(forms.ModelForm):
    class Meta:
        model = Referendum
        fields = ['title', 'description', 'choices', 'date_available', 'date_expired']

class VoterUpdateForm(forms.ModelForm):
    class Meta:
        model = Voter
        fields = ['username', 'first_name', 'last_name', 'email', 'phone']