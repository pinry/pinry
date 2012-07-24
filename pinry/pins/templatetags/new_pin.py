from django.template.loader import render_to_string
from django.template import Library
from django.template import RequestContext

from pinry.pins.forms import PinForm


register = Library()


@register.simple_tag
def new_pin(request):
    return render_to_string('pins/templatetags/new_pin.html',
        {'form': PinForm()},
        context_instance=RequestContext(request))
