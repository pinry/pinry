from django import forms

from django_images.models import Image


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('image',)
