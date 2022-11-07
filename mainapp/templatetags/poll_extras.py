from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    """ Custom template filter. Gets dict from avg_rating() and in_four_days(). """
    return dictionary.get(key)
