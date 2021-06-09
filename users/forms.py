from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser, Profile

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields =['username', 'email']

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email')

class ProfileForm(forms.ModelForm):
    bio = forms.CharField(required=True)
    image = forms.ImageField(required=False)

    class Meta:
        model = Profile
        fields = ['image', 'bio']

