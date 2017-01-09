from django import template

register = template.Library()


@register.filter
def get_pct(part, whole):
    try:
        return (part / whole) * 100
    except ZeroDivisionError:
        return 0.0
