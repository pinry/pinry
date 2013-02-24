from django import forms

from .models import Pin


class PinForm(forms.ModelForm):
    url = forms.CharField(required=False)
    image = forms.ImageField(label='or Upload', required=False)

    _errors = {
        'not_image': 'Requested URL is not an image file. Only images are currently supported.',
        'pinned': 'URL has already been pinned!',
        'protocol': 'Currently only support HTTP and HTTPS protocols, please be sure you include this in the URL.',
        'nothing': 'Need either a URL or Upload',
    }

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
                raise forms.ValidationError(self._errors['not_image'])
            protocol = url.split(':')[0]
            if protocol not in ['http', 'https']:
                raise forms.ValidationError(self._errors['protocol'])
            try:
                Pin.objects.get(url=url)
                raise forms.ValidationError(self._errors['pinned'])
            except Pin.DoesNotExist:
                pass
        elif image:
            pass
        else:
            raise forms.ValidationError(self._errors['nothing'])

        return cleaned_data
