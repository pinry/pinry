from django import forms

from taggit.forms import TagField

from .models import Pin


class PinForm(forms.Form):
    url = forms.CharField(label='URL', required=False)
    image = forms.ImageField(label='or Upload', required=False)
    description = forms.CharField(label='Description', required=False, widget=forms.Textarea)
    tags = TagField()

    def check_if_image(self, data):
        # Test file type
        image_file_types = ['png', 'gif', 'jpeg', 'jpg']
        file_type = data.split('.')[-1]
        if file_type.lower() not in image_file_types:
            raise forms.ValidationError("Requested URL is not an image file. "
                                        "Only images are currently supported.")

    def clean(self):
        cleaned_data = super(PinForm, self).clean()

        url = cleaned_data.get('url')
        image = cleaned_data.get('image')

        if url:
            self.check_if_image(url)
            try:
                Pin.objects.get(url=url)
                raise forms.ValidationError("URL has already been pinned!")
            except Pin.DoesNotExist:
                protocol = url.split(':')[0]
                if protocol == 'http':
                    opp_url = url.replace('http://', 'https://')
                elif protocol == 'https':
                    opp_url = url.replace('https://', 'http://')
                else:
                    raise forms.ValidationError("Currently only support HTTP and "
                                                "HTTPS protocols, please be sure "
                                                "you include this in the URL.")

                try:
                    Pin.objects.get(url=opp_url)
                    raise forms.ValidationError("URL has already been pinned!")
                except Pin.DoesNotExist:
                    pass
        elif image:
            pass
        else:
            raise forms.ValidationError("Need either a URL or Upload.")

        return cleaned_data
