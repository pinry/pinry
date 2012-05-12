from django import template
from django.template import loader, Context


register = template.Library()


@register.simple_tag
def bootstrap_field(field):
    t = loader.get_template('core/templatetags/bootstrap_field.html')
    return t.render(Context({'field': field}))
