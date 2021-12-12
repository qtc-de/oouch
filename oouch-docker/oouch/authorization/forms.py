from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    ssh_server = forms.CharField(max_length=100, required=False, help_text='Optional.')
    ssh_user = forms.CharField(max_length=100, required=False, help_text='Optional.')
    ssh_key = forms.CharField(max_length=500, required=False, help_text='Optional.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'ssh_server', 'ssh_user', 'ssh_key', 'password1', 'password2', )
