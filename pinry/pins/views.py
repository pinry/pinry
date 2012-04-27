from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from .models import Pin
from .forms import PinForm


def recent_pins(request):
    return TemplateResponse(request, 'pins/recent_pins.html', None)


def new_pin(request):
    if request.method == 'POST':
        form = PinForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('pins:recent-pins'))
    else:
        form = PinForm()
    context = {
        'form': form,
    }
    return TemplateResponse(request, 'pins/new_pin.html', context)
