import json

from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView

from braces.views import LoginRequiredMixin, JSONResponseMixin
from django_images.models import Image

from .forms import ImageForm


class CreateImage(JSONResponseMixin, LoginRequiredMixin, CreateView):
    template_name = None  # JavaScript-only view
    model = Image
    form_class = ImageForm

    def form_valid(self, form):
        image = form.save()
        return self.render_json_response({
            'success': {
                'id': image.id
            }
        })

    def form_invalid(self, form):
        return self.render_json_response({'error': form.errors})
