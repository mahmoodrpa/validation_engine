from django import template
import os

register = template.Library()

@register.filter
def format_currency(value):
    if value is None:
        return value
    try:
        value = float(value)
        return '${:,.2f}'.format(value)
    except (ValueError, TypeError):
        return value

@register.filter
def get_field_value(obj, field_name):
    return getattr(obj, field_name, '')

@register.filter
def format_quantity(value):
    if value is None:
        return value
    try:
        value = float(value)
        return '{:,.0f}'.format(value)
    except (ValueError, TypeError):
        return value
    
@register.filter
def format_rebate(value):
    if value is None:
        return value
    try:
        value = float(value)
        return '{:.2%}'.format(value)
    except (ValueError, TypeError):
        return value


@register.filter(name='filename')
def filename(value):
    return os.path.basename(value)