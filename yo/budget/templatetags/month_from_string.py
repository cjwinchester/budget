from django import template
from time import strptime, strftime

register = template.Library()

@register.filter
def monthyear(value):
    t = strptime(value, "%Y-%m-%d")
    return strftime("%B %Y", t)