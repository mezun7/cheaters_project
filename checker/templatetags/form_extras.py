from django import template

register = template.Library()


@register.filter()
def get_at_index_threshold(lst, index):
    return lst[int(index)]['threshold']
