from django import forms

from .models import Pin


class PinForm(forms.ModelForm):
    url = forms.CharField(label='URL')

    class Meta:
        model = Pin
        exclude = ['image']
