from django import forms

from .models import Pin


class PinForm(forms.ModelForm):
    url = forms.CharField(label='URL')

    def clean_url(self):
        data = self.cleaned_data['url']

        # Test file type
        image_file_types = ['png', 'gif', 'jpeg', 'jpg']
        file_type = data.split('.')[-1]
        if file_type.lower() not in image_file_types:
            raise forms.ValidationError("Requested URL is not an image file. "
                                        "Only images are currently supported.")

        # Check if pin already exists
        try:
            Pin.objects.get(url=data)
            raise forms.ValidationError("URL has already been pinned!")
        except Pin.DoesNotExist:
            protocol = data.split(':')[0]
            if protocol == 'http':
                opp_data = data.replace('http://', 'https://')
            elif protocol == 'https':
                opp_data = data.replace('https://', 'http://')
            else:
                raise forms.ValidationError("Currently only support HTTP and "
                                            "HTTPS protocols, please be sure "
                                            "you include this in the URL.")

            try:
                Pin.objects.get(url=opp_data)
                raise forms.ValidationError("URL has already been pinned!")
            except Pin.DoesNotExist:
                return data

    class Meta:
        model = Pin
        exclude = ['image']
