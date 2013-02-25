from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.utils.functional import lazy
from django.views.generic import (
    TemplateView, CreateView)

from django_images.models import Image

from .forms import ImageForm


reverse_lazy = lambda name=None, *args: lazy(reverse, str)(name, args=args)


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


class UploadImage(LoginRequiredMixin, CreateView):
    template_name = 'pins/pin_form.html'
    model = Image
    form_class = ImageForm

    def form_valid(self, form):
        messages.success(self.request, 'New pin successfully added.')
        return super(UploadImage, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Pin did not pass validation!')
        return super(UploadImage, self).form_invalid(form)


class RecentPins(TemplateView):
    template_name = 'pins/recent_pins.html'