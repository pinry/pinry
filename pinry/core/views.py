from django.contrib.auth.models import Permission
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.conf import settings

from .forms import UserCreationForm


def home(request):
    return HttpResponseRedirect(reverse('pins:recent-pins'))


def private(request):
    return TemplateResponse(request, 'core/private.html', None)


def register(request):
    if not settings.ALLOW_NEW_REGISTRATIONS:
        messages.error(request, "The admin of this service is not "
                                "allowing new registrations.")
        return HttpResponseRedirect(reverse('pins:recent-pins'))
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            permissions = Permission.objects.filter(codename__in=['add_pin', 'add_image'])
            user = form.save()
            user.user_permissions = permissions
            messages.success(request, 'Thank you for registering, you can now '
                                      'login.')
            return HttpResponseRedirect(reverse('core:login'))
    else:
        form = UserCreationForm()

    return TemplateResponse(request, 'core/register.html', {'form': form})


@login_required
def logout_user(request):
    logout(request)
    messages.success(request, 'You have successfully logged out.')
    return HttpResponseRedirect(reverse('core:home'))
