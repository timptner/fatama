from django import template

from congresses.models import Congress

register = template.Library()


@register.simple_tag
def current_year():
    """Get year of latest congress"""
    congress = Congress.objects.order_by('-year').first()
    return congress.year
