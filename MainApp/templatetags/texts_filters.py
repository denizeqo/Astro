from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    """Look up a dict key using a variable in templates."""
    if dictionary is None:
        return ""
    return dictionary.get(key, "")
