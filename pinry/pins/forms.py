from django import forms

from .models import Pin


class PinForm(forms.ModelForm):
    url = forms.CharField(required=False)
    image = forms.ImageField(label='or Upload', required=False)

    class Meta:
        model = Pin
        fields = ['url', 'image', 'description', 'tags']

    def clean(self):
        cleaned_data = super(PinForm, self).clean()

        url = cleaned_data.get('url')
        image = cleaned_data.get('image')

        if url:
            image_file_types = ['png', 'gif', 'jpeg', 'jpg']
            if not url.split('.')[-1].lower() in image_file_types:
                raise forms.ValidationError("Requested URL is not an image file. "
                                            "Only images are currently supported.")
            try:
                Pin.objects.get(url=url)
                raise forms.ValidationError("URL has already been pinned!")
            except Pin.DoesNotExist:
                pass
            protocol = url.split(':')[0]
            if protocol not in ['http', 'https']:
                raise forms.ValidationError("Currently only support HTTP and "
                                            "HTTPS protocols, please be sure "
                                            "you include this in the URL.")
            try:
                Pin.objects.get(url=url)
                raise forms.ValidationError("URL has already been pinned!")
            except Pin.DoesNotExist:
                pass
        elif image:
            pass
        else:
            raise forms.ValidationError("Need either a URL or Upload.")

        return cleaned_data
