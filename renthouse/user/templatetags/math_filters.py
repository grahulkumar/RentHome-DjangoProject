from django import template
from decimal import Decimal

register = template.Library()

@register.filter
def multi(value,arg):
    #converting our no of days in decimal b'coz price is in decimal
    return value *Decimal(arg)  

