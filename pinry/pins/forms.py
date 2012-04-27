from django import forms

from .models import Pin


class PinForm(forms.ModelForm):
    url = forms.CharField(label='URL')

    def clean_url(self):
        data = self.cleaned_data['url']
        try:
            Pin.objects.get(url=data)
            raise forms.ValidationError("URL has already been pinned!")
        except Pin.DoesNotExist:
            image_file_types = ['png', 'gif', 'jpeg', 'jpg']
            file_type = data.split('.')[-1]
            if file_type.lower() not in image_file_types:
                raise forms.ValidationError("Requested URL is not an image file. Only images are currently supported.")
            return data

    class Meta:
        model = Pin
        exclude = ['image']
