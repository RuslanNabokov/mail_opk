from django import template

register = template.Library()

from ..models import *

@register.simple_tag
def total_posts():
    return s



@register.filter(name='message_indentation')
def indentation(value, arg='s'):
    if arg == 's':
        return  str(int(value) * 0.6) + '%'
    else:
        return str(int(value) * 0.6+ int(arg)) + '%'

#@register.filter(name='tostring') {{ 'a'|tostring:'s'  }}
#def to_string(value,l):
#    return str(l)