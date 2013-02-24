from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.utils.functional import lazy
from django.views.generic.base import TemplateView
from django.views.generic import CreateView

from .forms import PinForm
from .models import Pin


reverse_lazy = lambda name=None, *args: lazy(reverse, str)(name, args=args)


class RecentPins(TemplateView):
    template_name = 'pins/recent_pins.html'


class NewPin(CreateView):
    model = Pin
    form_class = PinForm
    success_url = reverse_lazy('pins:recent-pins')

    def form_valid(self, form):
        form.instance.submitter = self.request.user
        messages.success(self.request, 'New pin successfully added.')
        return super(NewPin, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Pin did not pass validation!')
        return super(NewPin, self).form_invalid(form)


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
