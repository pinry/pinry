from django.utils import simplejson
from django.http import HttpResponse

from pinry.pins.models import Pin


def pins_recent(request, page=1):
    start_pin = abs(int(page) - 1) * 25
    end_pin = int(page) * 25

    pins = Pin.objects.order_by('-id')[start_pin:end_pin]
    recent_pins = []
    for pin in pins:
        recent_pins.append({
            'id': pin.id,
            'thumbnail': pin.image.url_200x1000,
            'original': pin.image.url,
            'description': pin.description,
        })

    return HttpResponse(simplejson.dumps(recent_pins), mimetype="application/json")
