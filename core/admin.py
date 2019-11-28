from django.contrib import admin

from .models import Pin, Board


class PinAdmin(admin.ModelAdmin):
    pass


admin.site.register(Pin, PinAdmin)
admin.site.register(Board)
