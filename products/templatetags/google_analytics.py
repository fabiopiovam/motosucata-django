"""A simple Django templatetag that return Google Analytics code.
"""
from django.conf import settings
from django import template

register = template.Library()

@register.simple_tag
def google_analytics():
    return settings.GOOGLE_ANALYTICS_CODE
