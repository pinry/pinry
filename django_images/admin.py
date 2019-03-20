from django.contrib import admin

from .models import Image
from .models import Thumbnail


admin.site.register(Image)
admin.site.register(Thumbnail)
