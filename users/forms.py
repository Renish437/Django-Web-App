
from django import forms
from .models import *

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']
        labels = {
            'realname': 'Real Name',
            'email': 'Email',
            'location': 'Location',
            'bio': 'Bio'
        }
        widgets ={
            'image': forms.FileInput(attrs={'accept':'image/*'}),
            'bio': forms.Textarea(attrs={'rows':3}),
        }
