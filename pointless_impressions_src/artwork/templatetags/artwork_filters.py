from django import template
import json


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


@register.filter
def framing_conditions_json(conditions):
    """
    Converts a list of framing conditions into a JSON string
    suitable for embedding in HTML data attributes.
    """
    framing_options = []
    for cond in conditions:
        framing_options.append({
            'id': cond.id,
            'name': cond.name,
            'slug': cond.slug
        })
    return json.dumps(framing_options)


@register.filter
def jsonify(value):
    """
    Converts any value to a JSON string suitable for embedding
    in HTML data attributes.

    Useful for converting Django queryset objects or other data
    to JSON for JavaScript access.
    """
    # Handle RelatedManager or QuerySet
    if hasattr(value, 'all') and callable(value.all):
        items = []
        for item in value.all():
            friendly_name = getattr(
                item, 'condition_friendly_name', None
            )
            condition_name = getattr(
                item, 'condition_name', None
            )
            name = friendly_name or condition_name or str(item)
            items.append({
                'id': int(item.id),
                'name': str(name),
                'slug': str(getattr(item, 'slug', '')),
            })
        return json.dumps(items)

    # Handle iterables (list, tuple, QuerySet without .all())
    try:
        # Try to iterate - if it's iterable and not a string/dict
        if hasattr(value, '__iter__') and not isinstance(
            value, (str, dict)
        ):
            items = []
            for item in value:
                # If item is a model instance
                if hasattr(item, 'id'):
                    friendly_name = getattr(
                        item, 'condition_friendly_name', None
                    )
                    condition_name = getattr(
                        item, 'condition_name', None
                    )
                    name = (
                        friendly_name or condition_name or str(item)
                    )
                    items.append({
                        'id': int(item.id),
                        'name': str(name),
                        'slug': str(getattr(item, 'slug', '')),
                    })
                else:
                    items.append(item)
            return json.dumps(items)
    except (TypeError, AttributeError):
        pass

    return json.dumps(value)
