from django import forms

class ProfileForm(forms.Form):
    name = forms.CharField(max_length = 25)
    password = forms.CharField(max_length=30)
    picture = forms.ImageField()