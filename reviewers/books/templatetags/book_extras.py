from django import template
register = template.Library()


@register.filter
def rangeFilter(num):
    str_of_num = str(num).split('.')
    return range(int(str_of_num[0]))


@register.filter
def index(sequence, position):
    return sequence[position]
