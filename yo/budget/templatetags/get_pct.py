from django import template

register = template.Library()


@register.filter
def get_pct(part, whole):
    return (part / whole) * 100
