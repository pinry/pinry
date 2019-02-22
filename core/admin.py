from django.contrib import admin

from .models import Pin


class PinAdmin(admin.ModelAdmin):
    pass


admin.site.register(Pin, PinAdmin)
