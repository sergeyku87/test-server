from django import template

import re

register = template.Library()

@register.filter
def extract(path):
    agreement = re.search(r"\d+", path)
    if agreement:
        return agreement.group()
    return None
