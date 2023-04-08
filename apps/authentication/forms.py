from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        # Include these fields
        fields = ['first_name', 'last_name', 'username', 'email', 'password1']

    def clean_email(self):
        input = self.cleaned_data.get('email')
        if User.objects.filter(email=input).exists():
            raise ValidationError("A user with that email already exists")
        return input
    
    def clean_password1(self):
        input = self.cleaned_data.get('password1')
        if len(input) < 8 or not any(x.isupper() for x in input) or not any(x.isdigit() for x in input) or input.isalpha():
            raise ValidationError("Password must be at least 8 characters long and be a combination of uppercase, lowercase and numbers.")
        return input

    def clean(self):
        super().clean()
        # Not using password2, so don't include errors
        del self._errors["password2"]