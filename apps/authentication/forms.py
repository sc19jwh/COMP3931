from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.contrib.auth.models import User

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        # Include these fields
        fields = ['first_name', 'last_name', 'username', 'email', 'password1']
    def clean(self):
        super().clean()
        # Not using password2, so don't include errors
        del self._errors["password2"]