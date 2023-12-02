from django.contrib.auth.forms import (
    UserCreationForm,
    PasswordResetForm,
    SetPasswordForm,
)
from django import forms
from .models import Voter
from referendaMain.models import Referendum
from .models import User
from django.contrib.auth import get_user_model


class CreateUserForm(UserCreationForm):
    email = forms.EmailField(
        required=True, error_messages={"required": "This field is required."}
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class ReferendumForm(forms.ModelForm):
    class Meta:
        model = Referendum
        fields = ["title", "description", "date_available", "date_expired"]


class VoterUpdateForm(forms.ModelForm):
    class Meta:
        model = Voter
        fields = ["username", "first_name", "last_name", "email", "phone"]


class SetPasswordForm(SetPasswordForm):
    class Meta:
        model = get_user_model()
        fields = ["new_password1", "new_password2"]


class CustomPasswordResetForm(PasswordResetForm):
    username = forms.CharField(
        max_length=254,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Username"}
        ),
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        email = cleaned_data.get("email")

        if not username and not email:
            raise forms.ValidationError("Please enter either your username or email.")

        if username:
            user = (
                get_user_model().objects.filter(username=username, email=email).first()
            )
        else:
            user = get_user_model().objects.filter(email=email).first()

        if not user:
            raise forms.ValidationError(
                "No user found with the provided username and email combination."
            )

        return cleaned_data
