from django import template

register = template.Library()


@register.filter
def choropleth_month_box(value, base_color):
    value = float(value)
    if base_color == "#d43f3a":
        if value == 0.0:
            return "#fff"
        elif 0.0 < value <= 25.0:
            return "#ddd"
        elif 25.0 < value <= 50.0:
            return "#ccc"
        elif 50.0 < value <= 75.0:
            return "#bbb"
        elif 75.0 < value <= 100.0:
            return "#aaa"
        elif 100.0 < value:
            return "#000"
    else:
        if value == 0.0:
            return "#fff"
        elif 0.0 < value <= 25.0:
            return "#ddd"
        elif 25.0 < value <= 50.0:
            return "#ccc"
        elif 50.0 < value <= 75.0:
            return "#bbb"
        elif 75.0 < value <= 100.0:
            return "#aaa"
        elif 100.0 < value:
            return "#000"
            
@register.filter
def textcolor(value, comparison):
    if float(value) > float(comparison):
        return "#fff"
    else:
        return "#111"