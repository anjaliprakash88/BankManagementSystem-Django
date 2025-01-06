from django import forms
from .models import user


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = user
        fields = ['name', 'address', 'image', 'phone', 'email', 'age', 'dob', 'pancard', 'adharcard']
