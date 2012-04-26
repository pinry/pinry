from django import forms

from .models import Pin


class PinForm(forms.ModelForm):
    url = forms.CharField(label='URL')
    title = forms.CharField(required=False)

    class Meta:
        model = Pin
        exclude = ['image']
