from django import template


register = template.Library()


# Create your custom filters here
@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    """
    Updates the query parameters of the current request URL
    with the provided keyword arguments.
    """
    query = context['request'].GET.copy()

    for key, value in kwargs.items():
        if value is None:
            query.pop(key, None)
        else:
            query[key] = value

    return query.urlencode()


@register.simple_tag(takes_context=True)
def is_sort_active(context, sort_key, direction='asc'):
    """
    Checks if the given sort key and direction are active in the
    current query parameters.
    """
    current_sort = context['request'].GET.get('sort', 'price')
    current_direction = context['request'].GET.get('direction', 'asc')

    return current_sort == sort_key and current_direction == direction
