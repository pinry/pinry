from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages

from .forms import PinForm
from .models import Pin


def recent_pins(request):
    return TemplateResponse(request, 'pins/recent_pins.html', None)


def new_pin(request):
    if request.method == 'POST':
        form = PinForm(request.POST, request.FILES)
        if form.is_valid():
            pin = form.save(commit=False)
            pin.submitter = request.user
            pin.save()
            messages.success(request, 'New pin successfully added.')
            return HttpResponseRedirect(reverse('pins:recent-pins'))
        else:
            messages.error(request, 'Pin did not pass validation!')
    else:
        form = PinForm()
    context = {
        'form': form,
    }
    return TemplateResponse(request, 'pins/new_pin.html', context)


def delete_pin(request, pin_id):
    try:
        pin = Pin.objects.get(id=pin_id)
        if pin.submitter == request.user:
            pin.delete()
            messages.success(request, 'Pin successfully deleted.')
        else:
            messages.error(request, 'You are not the submitter and can not '
                                    'delete this pin.')
    except Pin.DoesNotExist:
        messages.error(request, 'Pin with the given id does not exist.')
        

    return HttpResponseRedirect(reverse('pins:recent-pins'))
