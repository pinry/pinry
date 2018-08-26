from django import template

register = template.Library()


@register.filter
def at_size(image, size):
    return image.get_absolute_url(size=size)
