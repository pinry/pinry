from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect

from .models import Image, Thumbnail
from .settings import IMAGE_SIZES


def thumbnail(request, image_id, size):
    image = get_object_or_404(Image, id=image_id)
    if size not in IMAGE_SIZES:
        return HttpResponseNotFound()

    return redirect(Thumbnail.objects.get_or_create_at_size(image, size))
