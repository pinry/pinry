import json

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Permission
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponseBadRequest, HttpResponse
from django.template.response import TemplateResponse
from django.utils.functional import lazy
from django.views.generic import CreateView
from rest_framework.renderers import JSONRenderer

from core.serializers import UserSerializer
from .forms import UserCreationForm
from users.models import User


def reverse_lazy(name=None, *args):
    return lazy(reverse, str)(name, args=args)


class CreateUser(CreateView):
    template_name = 'users/register.html'
    model = User
    form_class = UserCreationForm
    success_url = reverse_lazy('core:recent-pins')

    def get(self, request, *args, **kwargs):
        if not settings.ALLOW_NEW_REGISTRATIONS:
            messages.error(request, "The admin of this service is not allowing new registrations.")
            return HttpResponseRedirect(reverse('core:recent-pins'))
        return super(CreateUser, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        redirect = super(CreateUser, self).form_valid(form)
        permissions = Permission.objects.filter(codename__in=['add_pin', 'add_image'])
        user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])
        user.user_permissions = permissions
        login(self.request, user)
        return redirect


def login_user(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return HttpResponseBadRequest()
    if 'username' not in data:
        return HttpResponseBadRequest(
            json.dumps({"username": "this field is required"})
        )
    if 'password' not in data:
        return HttpResponseBadRequest(
            json.dumps({"password": "this field is required"})
        )
    user = authenticate(
        request,
        username=data['username'],
        password=data['password']
    )
    if not user:
        return HttpResponseBadRequest(
            json.dumps({"password": "username and password doesn't match"})
        )
    login(request, user)
    data = UserSerializer(
        user,
        context={'request': request},
    ).data
    return HttpResponse(
        JSONRenderer().render(data),
        content_type="application/json"
    )


@login_required
def logout_user(request):
    logout(request)
    messages.success(request, 'You have successfully logged out.')
    return HttpResponseRedirect(reverse('core:recent-pins'))


def private(request):
    return TemplateResponse(request, 'users/private.html', None)
