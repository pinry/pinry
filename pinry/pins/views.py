import json

from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.utils.functional import lazy
from django.views.generic import CreateView

from django_images.models import Image

from .forms import ImageForm


class LoginRequiredMixin(object):
    """
    A login required mixin for use with class based views. This Class is a light wrapper around the
    `login_required` decorator and hence function parameters are just attributes defined on the class.

    Due to parent class order traversal this mixin must be added as the left most
    mixin of a view.

    The mixin has exactly the same flow as `login_required` decorator:

        If the user isn't logged in, redirect to settings.LOGIN_URL, passing the current
        absolute path in the query string. Example: /accounts/login/?next=/polls/3/.

        If the user is logged in, execute the view normally. The view code is free to
        assume the user is logged in.

    **Class Settings**
        `redirect_field_name - defaults to "next"
        `login_url` - the login url of your site

    """
    redirect_field_name = REDIRECT_FIELD_NAME
    login_url = None

    @method_decorator(login_required(redirect_field_name=redirect_field_name, login_url=login_url))
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)


class JSONResponseMixin(object):
    """
    A mixin that can be used to render a JSON response.
    """
    def render_to_response(self, context, **response_kwargs):
        """
        Returns a JSON response, transforming 'context' to make the payload.
        """
        response_kwargs['content_type'] = 'application/json'
        return HttpResponse(
            self.convert_context_to_json(context),
            **response_kwargs
        )

    def convert_context_to_json(self, context):
        """Convert the context dictionary into a JSON object"""
        return json.dumps(context)


class UploadImage(JSONResponseMixin, LoginRequiredMixin, CreateView):
    template_name = 'core/pin_form.html'
    model = Image
    form_class = ImageForm

    def form_valid(self, form):
        message = 'New pin successfully added.'
        if self.request.is_ajax():
            self.object = form.save()
            context = {'image_id': self.object.pk}
            return JSONResponseMixin.render_to_response(self, context)
        else:
            messages.success(self.request, message)
            return super(UploadImage, self).form_valid(form)

    def form_invalid(self, form):
        message = 'Pin did not pass validation!'
        if self.request.is_ajax():
            context = {'error': message}
            return JSONResponseMixin.render_to_response(self, context)
        else:
            messages.error(self.request, message)
            return super(UploadImage, self).form_invalid(form)
